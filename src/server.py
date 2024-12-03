#!/usr/bin/env python3
from __future__ import annotations

import socketserver
import mysql.connector
from os import getenv
from binascii import hexlify
from pathlib import Path
from dataclasses import field
from obj2bin import Const, Field, Child, pack, encode, decode

# ******************** api ********************

def strenc(s: str, l: int) -> bytes: return bytes(ord(s[i]) if i<len(s) else 0 for i in range(l))
def strdec(b: bytes, l: int) -> str: return "".join(map(chr, b[:l]))

# TODO: come up with a cleaner API definition
ACK_ID = 0x01
SCORE_ID = 0x02
SCORE_LIST_ID = 0x03
SCORE_REQ = 0x04
SCORE_PUB = 0x05

@pack(_id=Const(ACK_ID, "B"))
class Ack: pass

@pack(_id=Const(_id:=0x01, "B"), player=Field("<6s", enc=lambda x: strenc(x, 6), dec=lambda x: strdec(x, 6)), score=Field("<L"))
class Score: player: str; score: int

@pack(_id=Const(SCORE_LIST_ID, "B"), score_count=Field("H", meta=True), scores=Child(Score, count="score_count"))
class ScoreList:
  scores: list[Score] = field(default_factory=list)
  @property
  def score_count(self) -> int: return len(self.scores)

@pack(_id=Const(SCORE_REQ, "B"), count=Field("H"))
class ScoreReq: count: int

@pack(_id=Const(SCORE_PUB, "B"), score=Child(Score))
class ScorePub: score: Score

DF = { ACK_ID: Ack, SCORE_ID: Score, SCORE_LIST_ID: ScoreList, SCORE_REQ: ScoreReq, SCORE_PUB: ScorePub }
def df(buff: bytes) -> tuple: return decode(DF[buff[0]], buff) if buff[0] in DF else (None, 0)

# ******************** server ********************

DEBUG, HOST, PORT = int(getenv("DEBUG", "0")), getenv("HOST", "127.0.0.1"), int(getenv("PORT", "6969"))

db_opts = { "host": "127.0.0.1" }
DB_ENV_OPTS = { "MYSQL_DATABASE": "database", "MYSQL_USER": "user", "MYSQL_PASSWORD": "password", "MYSQL_PORT": "port" }
with Path("db/.env").open() as f: db_opts.update({ DB_ENV_OPTS[k]: v for k, v in (l.strip().split("=") for l in f) if k in DB_ENV_OPTS})
conn = mysql.connector.connect(**db_opts)

class TCPHandler(socketserver.BaseRequestHandler):
  def handle(self):
    cid = "[" + ":".join(map(str, self.client_address)) + "]"
    print(f"{cid} connection opened")
    try:
      while (data := self.request.recv(1024)):
        if DEBUG > 0: print(f"{cid} recv {len(data)}B: {hexlify(data).decode()}")
        try:
          recv, sz = df(data)
          assert recv, "unkown packet type"
          print(f"{cid} -> {recv}")
          resp: object | None = None
          match recv:
            case ScoreReq():
              with conn.cursor() as curr:
                curr.execute("select player, score from score order by score desc limit %s", (recv.count if recv.count > 0 else 5,))
                resp = ScoreList([Score(*x) for x in curr.fetchall()]) # type: ignore[call-arg]
            case ScorePub():
              with conn.cursor() as curr:
                curr.execute("insert into score (player, score) values (%s, %s)", (recv.score.player, recv.score.score))
                conn.commit()
                resp = Ack()
          if resp is None: continue
          print(f"{cid} <- {resp}")
          data, sz = encode(resp)
          if DEBUG > 0: print(f"{cid} send {sz}B: {hexlify(data).decode()}")
          self.request.sendall(data)
        except Exception as e:
          print(f"{cid} invalid packet received : {e}")
    except ConnectionResetError:
      pass
    print(f"{cid} connection closed")

if __name__ == "__main__":
  HOST, PORT = getenv("HOST", "127.0.0.1"), int(getenv("PORT", "6969"))
  server = socketserver.TCPServer((HOST, PORT), TCPHandler)
  print(f"server listening on: {HOST}:{PORT}")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print("\nserver stopped by user")
  finally:
    conn.close()

import socket
from os import getenv
from binascii import hexlify
from server import df, ScoreReq, ScorePub, Score, ScoreList
from obj2bin import encode

def tohex(d): return hexlify(d).decode()

HOST, PORT = getenv("HOST", "127.0.0.1"), int(getenv("PORT", "6969"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  data, _ = encode(ScorePub(Score("TEST", 69420)))
  print(f"send: {tohex(data)}")
  s.sendall(data)
  recv = s.recv(1024)
  print(f"recv: {tohex(recv)}")
  print(df(recv)[0])

  data, _ = encode(ScoreReq(10))
  print(f"send: {tohex(data)}")
  s.sendall(data)
  recv = s.recv(1024)
  print(f"recv: {tohex(recv)}")
  for score in df(recv)[0].scores:
    print(score)

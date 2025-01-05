import socket
from os import getenv
from binascii import hexlify
from server import df_decode, ScoreReq, ScoreType
from obj2bin import encode

def tohex(d): return hexlify(d).decode()

HOST, PORT = getenv("HOST", "127.0.0.1"), int(getenv("PORT", "6969"))

print(f"connecting to {HOST}:{PORT}")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  data, _ = encode(ScoreReq(ScoreType.A, 5))
  print(f"send: {tohex(data)}")
  s.sendall(data)
  s.settimeout(2)
  recv = s.recv(1024)
  print(f"recv: {tohex(recv)}")
  for score in df_decode(recv)[0].scores: print(score)

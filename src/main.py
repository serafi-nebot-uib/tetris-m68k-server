import mysql.connector
from pathlib import Path

db_opts = { "host": "127.0.0.1" }
DB_ENV_OPTS = { "MYSQL_DATABASE": "database", "MYSQL_USER": "user", "MYSQL_PASSWORD": "password", "MYSQL_PORT": "port" }
with Path("db/.env").open() as f: db_opts.update({ DB_ENV_OPTS[k]: v for k, v in (l.strip().split("=") for l in f) if k in DB_ENV_OPTS})

with mysql.connector.connect(**db_opts) as conn, conn.cursor() as cur:
  cur.execute("select * from score")
  while data := cur.fetchone(): print("\t".join(map(str, data)))

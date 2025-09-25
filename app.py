# app.py
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()
conninfo = os.environ["DATABASE_URL"]  # includes sslmode=require

with psycopg.connect(conninfo) as conn:
    with conn.cursor() as cur:
        cur.execute("select version();")
        print(cur.fetchone())


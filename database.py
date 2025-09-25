""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os
from datetime import datetime

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def add_guestbook_entry(name, message):
    """Add a new guestbook entry"""
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding guestbook entry from %s", name)
        cur.execute(
            "INSERT INTO guestbook (name, message, created_at) VALUES (%s, %s, %s)", 
            (name, message, datetime.now())
        )

def get_guestbook_entries(page=0, entries_per_page=10):
    """Get guestbook entries with pagination"""
    limit = entries_per_page
    offset = page * entries_per_page
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT * FROM guestbook ORDER BY created_at DESC LIMIT %s OFFSET %s", 
            (limit, offset)
        )
        return cur.fetchall()

def get_guestbook_count():
    """Get total number of guestbook entries"""
    with get_db_cursor() as cur:
        cur.execute("SELECT COUNT(*) as count FROM guestbook")
        result = cur.fetchone()
        return result['count'] if result else 0

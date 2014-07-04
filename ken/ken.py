#!/usr/bin/env python

"""
Author: Haitham Gad
Date: July 3, 2014
Description: An application to help memorize vocabulary words
"""

import getopt
import sqlite3
import sys

# Model
class ken_db(object):
  class db_impl(object):
    def __init__(self, dbname):
      self.conn = sqlite3.connect(dbname)
      self.cur  = self.conn.cursor()
      self.create(self.cur)

    def create(self, cur):
      cur.execute('''
        CREATE TABLE IF NOT EXISTS words (
          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          word VARCHAR(30) NOT NULL,
          type CHAR(9) NOT NULL,
          definition TEXT,
          mnemonic VARCHAR(30),
          sentence TEXT,
          last_checked DATE NOT NULL,
          retention_counter INT(1) NOT NULL,
          retention_factor FLOAT(2, 2) NOT NULL DEFAULT 0.99
        )''')

      cur.execute('''
        CREATE TABLE IF NOT EXISTS synonyms (
          word_id1 INT(10) NOT NULL,
          word_id2 INT(10) NOT NULL,
          correlation FLOAT(2, 2) NOT NULL DEFAULT 0.99,
          PRIMARY KEY (word_id1, word_id2),
          FOREIGN KEY (word_id1) REFERENCES words(id) ON DELETE CASCADE,
          FOREIGN KEY (word_id2) REFERENCES words(id) ON DELETE CASCADE
        )''')

    def cleanup(self):
      self.conn.close()

  def __init__(self, dbname):
    self.dbname = dbname

  def __enter__(self):
    self.impl = self.db_impl(self.dbname)

  def __exit__(self, type, value, traceback):
    self.impl.cleanup()


class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg


def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
      raise Usage(msg)
    # more code, unchanged
    with ken_db('ken_db.db') as db:
      pass
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())


# -*- coding: utf-8 -*-

import sqlite3
import os.path


db_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
print('db file: %s', db_file)

def create_table_audios():
  db = sqlite3.connect(db_file)
  cur = db.cursor()

  db.execute(''' 
    create table if not exists audio_files ( 
      id int primary key, category  varchar(255), title varchar(255), 
      ilename  varchar(255), url text)
  ''')
  db.commit()
  db.close()


def main():
  create_table_audios()


if __name__ == '__main__':
  main()
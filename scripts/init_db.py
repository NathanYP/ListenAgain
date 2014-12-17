# -*- coding: utf-8 -*-

import sqlite3
import os.path


db_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')

sql = """ 
  drop table audio_files; \

  create table if not exists audio_files (\
    id        int primary key,\
    category  varchar(255),\
    title     varchar(255),\
    filename  varchar(255),\
    url       text\
  );\

  insert into audio_files(category, title, filename, url) values (\
    'elllo.org', 'test', 'test', 'test'
  );
"""

def main():
  db = sqlite3.connect(db_file)
  cur = db.cursor()

  cur.executescript(sql)
  print('table created')
  db.commit()

  db.execute('SELECT count(*) from audio_files')
  data = cur.fetchall()
  print(len(data))

  cur.close()
  db.close()


if __name__ == '__main__':
  main()
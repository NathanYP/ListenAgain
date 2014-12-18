# -*- coding: utf-8 -*-

import sys
import os.path
import urllib2
import re
import json
import logging
import sqlite3

from bs4 import BeautifulSoup

data_home = os.path.join(os.path.dirname(__file__), '..', 'data')
index_file = os.path.join(data_home, 'elllo.json')
data_folder = os.path.join(data_home, 'elllo')

db_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
db = sqlite3.connect(db_file)
cursor = db.cursor()

# db
def create_db_table():
  cursor.execute(''' 
    create table if not exists audio_files ( 
      id int primary key, category  varchar(255), title varchar(255), 
      filename  varchar(255), url text)
  ''')
  db.commit()


def has_downloaded(page):
  cursor.execute('''SELECT count(*) from audio_files where url = ?''', (page,))
  row = cursor.fetchone()
  return row[0] == 1

def insert_into(filename, page):
  pass

# crawler
def get_soup(url):
  response = urllib2.urlopen(url)
  return BeautifulSoup(response.read())


def collect_index_pages():
  head_soup = get_soup('http://www.elllo.org/english/0001.htm')

  head_pages = []
  for item in head_soup.find_all('div', class_='listgroup'):
    head_pages.append('http://www.elllo.org/english/' + item.contents[0]['href'])

  pages = set()
  for page in reversed(head_pages):
    matched = re.search('(\d+)\.htm$', page)
    page_index = matched.group(1)

    soup = get_soup(page)
    for item in soup.find_all('a', href=re.compile('^' + page_index + '\/')):
      pages.add('http://www.elllo.org/english/' + item['href'])
    break

  return pages


def parse_and_download(page):
  soup = get_soup(page)

  audio_file = None
  ogg = soup.find('source', type='audio/ogg')
  if ogg:
    audio_file = download_audio(ogg['src'])

  transcript = list()
  container = soup.find('div', id='transcript', class_='transcript')
  for item in container.find_all('p'):
    contents = list(item.stripped_strings)
    if len(contents) == 1:
      transcript.append({'name': None, 'transcript': ' '.join(contents)})
    else:
      transcript.append({'name': contents[0], 'transcript': ' '.join(contents[1:])})

  print(transcript)


def download_audio(link):
  filename = os.path.basename(link)
  local_file = os.path.join(data_folder, filename)
  CHUNK = 4 *1024

  req = urllib2.urlopen(url)
  with open(local_file, 'wb') as fp:
    while True:
      chunk = req.read(CHUNK)
      if not chunk:
        break
      else:
        fp.write(chunk)

  return local_file

def main():
  create_db_table()

  all_pages = collect_index_pages()
  for page in all_pages:
    if not has_downloaded(page):
      try:
        print("{0} - downloading".format(page))
        parse_and_download(page)
      except:
        print("{0} - failed, {1}".format(page, sys.exc_info()[0]))


if __name__ == '__main__':
  main()
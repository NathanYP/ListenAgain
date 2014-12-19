# -*- coding: utf-8 -*-

import sys
import os
import re
import os.path
import urllib2
import urlparse
import json
import logging
import sqlite3

from bs4 import BeautifulSoup


data_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'elllo')
if not os.path.exists(data_folder):
  os.mkdir(data_folder)

db_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
db = sqlite3.connect(db_file)
cursor = db.cursor()

# db
def create_db_table():
  cursor.execute(''' 
    create table if not exists audio_files ( 
      id integer primary key, category  varchar(255), title varchar(255), 
      filename varchar(255), page_link text, transcript text)
  ''')
  db.commit()


def has_downloaded(page_link):
  cursor.execute('''SELECT count(*) from audio_files where page_link = ?''', (page_link,))
  row = cursor.fetchone()
  return row[0] == 1

def insert_into(category, filename, page_link, transcript):
  cursor.execute('''INSERT INTO audio_files (category, title, filename, page_link, transcript) 
                    VALUES (NULL, ?, ?, ?, ?)''', (category, filename, page_link, transcript))
  db.commit()

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

    return audio_file, transcript
  else:
    return None, None


def download_audio(link):
  filename = os.path.basename(link)
  local_file = os.path.join(data_folder, filename)
  CHUNK = 4 *1024

  req = urllib2.urlopen(link)
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
  for index, page in enumerate(all_pages):
    if not has_downloaded(page):
      try:
        print("{0} - downloading".format(page))

        audio_file, transcript = parse_and_download(page)
        if audio_file:
          uri = urlparse.urlparse(page)
          filename = os.path.basename(audio_file)

          insert_into(uri.netloc, filename, page, json.dumps(transcript))

        print("{0} - downloaded\n".format(page))
      except Exception as e:
        print("{0} - failed".format(page))
        print(e)
        print("\n")

    if index >= 5:
      break


if __name__ == '__main__':
  main()
# -*- coding: utf-8 -*-

import os.path
import urllib2
import re
import json
import logging

from bs4 import BeautifulSoup

data_home = os.path.join(os.path.dirname(__file__), '..', 'data')
index_file = os.path.join(data_home, 'elllo.json')
data_folder = os.path.join(data_home, 'elllo')


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

  for p in pages:
    parse_page(p)
    break


def parse_page(url):
  soup = get_soup(url)

  ogg = soup.find('source', type='audio/ogg')
  if ogg:
    download_audio(ogg['src'])

  transcript = list()
  container = soup.find('div', id='transcript', class_='transcript')
  for item in container.find_all('p'):
    if len(item.strings) == 1:
      transcript.append({'name': None, item.strings.join('')})
    else:


    # for string in item.strings:
    #   print(repr(string))
    # print('---')


# def read_index_file():
#   if not os.path.exists(index_file):
#     with open(index_file, 'w') as file:
#       json.dump(list(), file)

#   existed = None
#   with open(index_file, 'r') as file:
#     existed = 


# def write_index_file():
#   pass

def main():
  # existed = read_index_file()
  collect_index_pages()

if __name__ == '__main__':
  collect_index_pages()
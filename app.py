# -*- coding: utf-8 -*-

import os.path
import sqlite3
import json

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop


from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)
define('home', default=os.path.dirname(__file__), help='home directory of profile', type=str)

# db
def _execute(query):
  db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
  db = sqlite3.connect(db_path)
  cursor = db.cursor()

  try:
    cursor.execute(query)
    result = cursor.fetchall()
    db.commit()
  except Exception:
    raise

  db.close()
  return result


# Controllers

class HomeHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('home.html')


class EllloHandler(tornado.web.RequestHandler):
  def get(self):
    data = []

    rows = _execute('SELECT id, title, filename, transcript FROM audio_files ORDER BY id')
    for row in rows:
      _id, _title, _filename, _transcript = row 
      data.append( {'id': _id, 'title': _title, 'filename': _filename, 'transcript': _transcript} )

    self.write(json.dumps(data))


# class FileHandler(tornado.web.RequestHandler):
#   def get(self):
#     filename = os.path.join(os.path.dirname('__file__'), 'data', self.get_argument('name'))
#     with open(filename, 'rb') as f:
#       while True:
#         data = f.read(16384)
#         if not data:
#           break
#         self.write(data)
#     self.finish()


# Main
class Application(tornado.web.Application):
  def __init__(self):
    url_patterns = [
      (r'/', HomeHandler),
      (r'/elllo', EllloHandler),
    ]
    settings = dict(
      template_path = os.path.join(options.home, 'templates'),
      static_path = os.path.join(options.home, 'static'),
      debug = True,
    )
    tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
  main()  
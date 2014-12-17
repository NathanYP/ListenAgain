# -*- coding: utf-8 -*-

import os.path

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop


from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)
define('home', default=os.path.dirname(__file__), help='home directory of profile', type=str)


from urls import url_patterns


class Application(tornado.web.Application):
  def __init__(self):
    settings = dict(
      template_path = os.path.join(options.home, 'templates'),
      static_path = os.path.join(options.home, 'static'),
      debug = True,
    )
    tornado.web.Application.__init__(self, url_patterns, **settings)


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


def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
  main()  
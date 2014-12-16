# -*- coding: utf-8 -*-

import os.path

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop


from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r'/', HomeHandler),
    ]
    settings = dict(
      template_path = os.path.join(os.path.dirname(__file__), 'templates'),
      static_path = os.path.join(os.path.dirname(__file__), 'static'),
    )
    tornado.web.Application.__init__(self, handlers, **settings)


class HomeHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('home.html')


if __name__ == '__main__':
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
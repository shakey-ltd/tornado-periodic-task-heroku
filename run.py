import datetime
import os.path
import tornado.escape
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.options
import tornado.web
import redis

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

class Log(object):
    def __init__(self, text):
        super(Log, self).__init__()
        self.timestamp = datetime.datetime.now().isoformat()
        self.text = text

    def __unicode__(self):
        return '{0},{1}'.format(self.timestamp,self.text)

class RedisStore(object):
    callbacks = []

    def __init__(self):
        super(RedisStore, self).__init__()
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        self.redis = redis.from_url(redis_url)
        self.log_db = 'log'

    def add(self, item):
        self.redis.lpush(self.log_db, str(item))
        self.notifyCallbacks()

    def list(self):
        return self.redis.llen(self.log_db)

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

    def notifyCallbacks(self):
        for callback in self.callbacks:
            callback(self.list())


class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            (r'/', MainHandler),
            (r'/logs', StatusHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
            autoescape=None
            )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        count = self.application.db.list()
        self.render("index.html", count=count)

class StatusHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.db.register(self.callback)

    def on_close(self):
        self.application.db.unregister(self.callback)

    def on_message(self, message):
        pass

    def callback(self, count):
        self.write_message('{"count":"%d"}' % count)


def update():
    l = Log('new')
    db.add(l)

db = RedisStore()

tornado.options.parse_command_line()
http_server = tornado.httpserver.HTTPServer(Application(db))
http_server.listen(options.port)
ioloop = tornado.ioloop.IOLoop.instance()

# background update every 15 seconds
task = tornado.ioloop.PeriodicCallback(update,15*1000)
task.start()

ioloop.start()
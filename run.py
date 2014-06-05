from tornado import web, websocket, httpserver, ioloop
import os, datetime, json
import redis

class Log(object):
    def __init__(self, text):
        super(Log, self).__init__()
        utc_datetime = datetime.datetime.utcnow()
        self.timestamp = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.text = text

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

class RedisLog(object):
    callbacks = []

    def __init__(self):
        super(RedisLog, self).__init__()
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        self.redis = redis.from_url(redis_url)
        self.log_db = 'log'

    def add(self, log):
        self.redis.lpush(self.log_db, log.json())
        self.notifyCallbacks(log.json())

    def list(self):
        # read data
        data = self.redis.lrange(self.log_db, 0, 9)
        # decode json strings
        data = [json.loads(e) for e in data]
        return data

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

    def notifyCallbacks(self, log):
        for callback in self.callbacks:
            callback(log)


class Application(web.Application):
    def __init__(self):
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
        self.db = RedisLog()
        web.Application.__init__(self, handlers, **settings)

    def update(self):
        l = Log('update done')
        self.db.add(l)

class MainHandler(web.RequestHandler):
    def get(self):
        logs = self.application.db.list()
        self.render("index.html", logs=logs)

class StatusHandler(websocket.WebSocketHandler):
    def open(self):
        self.application.db.register(self.callback)

    def on_close(self):
        self.application.db.unregister(self.callback)

    def on_message(self, message):
        pass

    def callback(self, log):
        self.write_message(log)

def main():
    app = Application()
    server = httpserver.HTTPServer(app)
    server.listen(os.getenv("PORT", 5000))
    server_loop = ioloop.IOLoop.instance()

    # background update every 15 seconds
    task = ioloop.PeriodicCallback(app.update,15*1000)
    task.start()

    server_loop.start()

if __name__ == '__main__':
    main()
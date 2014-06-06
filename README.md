# Periodic tasks with Tornado and Redis. Heroku ready

#### Simple Tornado server running periodic task with Redis log and websocket console

Note: It's for educational purposes only. Not suitable for production.

## Setup

#### 1. Env

```
    $ git clone https://github.com/shakey-uk/tornado-periodic-task-heroku.git
    $ cd tornado-periodic-task-heroku
    $ virutalenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```

You can run it locally now (don't forget to start redis-server first):

```
    $ python run.py
```

#### 2. Heroku

```
    $ heroku create
    $ heroku addons:add redistogo
    $ heroku labs:enable websockets
    $ git push heroku master
    $ heroku ps:scale web=1
```

#### 3. Keep heroku alive

You can try NewRelic Heroku addon or http://uptimerobot.com. Here's instructions for NewRelic:

```
    $ heroku addons:add newrelic
    $ echo web: newrelic-admin run-program python run.py > Procfile
    $ heroku config:set NEW_RELIC_APP_NAME='tornado-tasks'
    $ heroku addons:open newrelic
```

Click the Settings tab, then click Availability Monitoring. In the URL To Ping text box add your app's url and click start pinging.

Done and done. :)


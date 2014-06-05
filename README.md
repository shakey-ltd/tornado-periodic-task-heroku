# Periodically perform tasks with Tornado

#### Simple Tornado server running periodic task with Redis log and websocket console


## Setup

#### 1. Project

```
    $ heroku create
    $ heroku addons:add redistogo
    $ heroku ps:scale web=1
    $ heroku labs:enable websockets
```

#### 1. Heroku

```
    $ heroku create
    $ heroku addons:add redistogo
    $ heroku labs:enable websockets
    $ git push heroku master
    $ heroku ps:scale web=1
```

#### 2. Use UptimeRobot to keep dyno alive

uptimerobot.com
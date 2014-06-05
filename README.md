# Periodically perform tasks with Tornado

#### Uses Redis for log


## Setup

#### 1. Heroku

```
    $ heroku create
    $ heroku addons:add redistogo
    $ heroku ps:scale web=1
    $ heroku labs:enable websockets
```

#### 2. Use UptimeRobot to keep dynos alive

uptimerobot.com
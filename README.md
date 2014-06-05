# Periodically perform tasks with Tornado

#### Uses Redis for log, Newrelics for monitoring


## Setup

#### 1. Heroku

```
    $ heroku create
    $ heroku addons:add redistogo
    $ heroku addons:add newrelic
    $ heroku ps:scale web=1
```


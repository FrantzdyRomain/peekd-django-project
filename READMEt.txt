**To be implemented**
Oauth for API security.
More coding for functionality
Design
**to test API calls using CURL(not secured)**

--Add Item
curl --dump-header - -H 
"Content-Type: application/json" -X POST --data '{"created_date": "T2015-02-26T00:17:20", "description": "BAngo Post", "image": "/media/items/None/flatpageadmin_1.png", "name": "Another Post", "user": null, "price":"10.5000"}' http://localhost:8000/api/v1/items/

Add User--
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"date_joined": "2013-03-02T01:20:21.260484", "email": "frank@email.com", "last_login": "/2015-03-02T01:20:21.260458", "password": "abc", "username": "POST"}' http://localhost:8000/api/v1/user/
Template Dictionary
{"created_date": "T2013-02-26T00:17:20", "description": “test Post", "image": "/media/items/None/flatpageadmin_1.png", "name": "Another Post", "user": "null", "price":"10.5000"}
























Dependencies
Django 1.3+
django-south
Mysql
Redis --for backend sessions
django-tastypie --For API

to get redis:
wget http://redis.googlecode.com/files/redis-2.6.6.tar.gz

sudo apt-get install build-essential
wget http://redis.googlecode.com/files/redis-2.2.13.tar.gz
tar -zxf redis-2.6.6.tar.gz
cd redis-2.6.6
make

Now you can run Redis just like that:

src/redis-server

But you probably want to add it to supervisor, runit or something like that instead. We should also install the python library:

pip install redis

Your Django website already uses sessions, and it results in making a query to your database on most pages. So if you make Redis handle sessions instead, you will make the website more healthy right away.

Install django-redis-sessions. They aren’t on PyPi if I’m not mistaken, let’s just use pip’s superpowers:

pip install git+https://github.com/martinrusev/django-redis-sessions
Configure Django now:

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
Use it for cache

You don’t need to kill your harddrive by using it for caching, and you don’t need any old-fashioned Memcached servers. Just use Redis!

pip install django-redis-cache
And add this to your settings:

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': 1,
        },
    },
}
As you have noticed, I’ve used different databases for cache and sessions. By default, Redis has 16 databases for you to use - no need to configure further. However, you can just put everything into a single database if you fell like it.

####################very importtant################
TO get redis working on every boot
--you must copy redis init script from utils directory into /etc/init.d dir on ubuntu
example
frantzdy@ubuntu:~/redis-2.6.6/utils$ sudo cp redis_init_script /etc/init.d/
################API STUFF ######################
POST--As with all Tastypie requests, the headers we request are important. 
Since we’ve been using primarily JSON throughout, let’s send a new entry in JSON format:
Tastypie also gives you full write capabilities in the API. 
Since the ItemResource has the no-limits Authentication & Authorization on it, we can freely write data.

--Add Item
curl --dump-header - -H 
"Content-Type: application/json" -X POST --data '{"created_date": "T2013-02-26T00:17:20", "description": "BAngo Post", "image": "/media/items/None/flatpageadmin_1.png", "name": "Another Post", "user": null, "price":"10.5000"}' http://localhost:8000/api/v1/items/

Add User--
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"date_joined": "2013-03-02T01:20:21.260484", "email": "frank@email.com", "last_login": "/2013-03-02T01:20:21.260458", "password": "abc", "username": "POST"}' http://localhost:8000/api/v1/user/
Template Dictionary
{"created_date": "T2013-02-26T00:17:20", "description": "BAngo Post", "image": "/media/items/None/flatpageadmin_1.png", "name": "Another Post", "user": "null", "price":"10.5000"}

***For logging in we can pass login credentials via json to url form?
http://stackoverflow.com/questions/11770501/how-can-i-login-to-django-using-tastypie


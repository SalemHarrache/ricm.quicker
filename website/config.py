# -*- coding: utf-8 -*-
'''
    :copyright: Copyright 2013 Salem Harrache.
    :license: BSD, see LICENSE for details.

'''
import uuid


class DevConfig(object):
    '''Dev configuration.'''

    SERVER_PATH = "http://localhost"
    SECRET_KEY = str(uuid.uuid4())

    SQLALCHEMY_ECHO = True

    # SQLite Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

    CACHE_TYPE = "null"
    CACHE_KEY_PREFIX = "ricm_quicker"
    CACHE_DEFAULT_TIMEOUT = 7200

    # Server
    DEBUG = True
    TESTING = False
    PORT = 9090
    HOST = "127.0.0.1"

    UNIVERSITY = "Polytech'Grenoble"


class ProdConfig(DevConfig):
    '''Dev configuration.'''

    SECRET_KEY = "myscret"

    SQLALCHEMY_ECHO = False

    # PostgreSQL Database
    DBUSER = "ricm_quicker"
    DBPASSWORD = "ricm_quicker"
    DBNAME = "ricm_quicker"
    DBHOST = "localhost"
    SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s/%s" % (
        DBUSER, DBPASSWORD, DBHOST, DBNAME)

    CACHE_TYPE = "simple"

    # Debug
    DEBUG = False
    TESTING = False
    # redis
    # CACHE_TYPE = "redis"
    # CACHE_REDIS_HOST = "localhost"

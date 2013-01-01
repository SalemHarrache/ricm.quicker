# -*- coding: utf-8 -*-
'''
    :copyright: Copyright 2013 Salem Harrache.
    :license: BSD, see LICENSE for details.

'''
from __future__ import division, unicode_literals

from flask_sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache


db = SQLAlchemy()
cache = Cache()

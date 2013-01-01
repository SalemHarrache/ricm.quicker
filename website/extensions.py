# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from flask_sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache


db = SQLAlchemy()
cache = Cache()

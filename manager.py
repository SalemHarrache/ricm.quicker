#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey

monkey.patch_all()

import requests

from flask import current_app, url_for
from flask_script import Manager, prompt_bool
from werkzeug.contrib.fixers import ProxyFix
from gevent.wsgi import WSGIServer
from website.model import (Site, Year, Group, Schedule, ScheduleGroupIcal,
                           ScheduleImage)
from website.app import app, db, configured_app
from website.config import DevConfig, ProdConfig
from website.data import init_database


def create_app_manager(config):
    if config == "prod":
        return configured_app(app, ProdConfig())
    else:
        return configured_app(app, DevConfig())


manager = Manager(create_app_manager)


@manager.command
def initdb():
    "Creates database tables and insert data"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        db.create_all()
        init_database()


@manager.command
def updatecache():
    "Update cache"
    urls = [url_for('clear_cache')]
    for year in Year.query.all():
        for group in year.groups:
            urls.append(url_for('index',
                                year=year.name,
                                group_name=group.name))
            urls.append(url_for('ical',
                                year=year.name,
                                group_name=group.name))
            for offset in range(-2, 6):
                urls.append(url_for('index',
                                    year=year.name,
                                    group_name=group.name,
                                    offset=offset))
    for url in urls:
        s = requests.session()
        url = "http://%s:%s%s" % (app.config['HOST'],
                                  app.config['PORT'],
                                  url)
        s.get(url)
        print url


def make_shell_context():
    return dict(app=current_app, db=db, Site=Site, Year=Year, Group=Group,
                Schedule=Schedule, ScheduleGroupIcal=ScheduleGroupIcal,
                ScheduleImage=ScheduleImage)


manager.add_option('-c', '--config',
                   dest="config",
                   required=True,
                   default='dev',
                   choices=('prod', 'dev'))


@manager.command
def runserver():
    """Runs the Flask server"""
    if app.debug:
        app.run(host=app.config['HOST'], port=app.config['PORT'])
    else:
        app.wsgi_app = ProxyFix(app.wsgi_app)
        address = app.config['HOST'], app.config['PORT']
        server = WSGIServer(address, app)
        try:
            print "Server running on port %s:%d. Ctrl+C to quit" % address
            server.serve_forever()
        except KeyboardInterrupt:
            server.stop()
    print "\nBye bye"


if __name__ == "__main__":
    manager.run()

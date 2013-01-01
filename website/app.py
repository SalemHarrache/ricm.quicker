# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
import StringIO


from flask import Flask, render_template, send_file, flash

from .model import Year, Group
from .extensions import db, cache


def configured_app(app, config):
    app.config.from_object(config)
    db.init_app(app)
    cache.init_app(app)
    if app.debug or app.testing:
        @app.errorhandler(400)
        def handle_bad_request_in_debug(exception):
            '''Add a request handler to debug 400 'Bad Request' exceptions.'''
            raise
    return app


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    flash("Cette page n'existe pas.", "error")
    years = list(Year.query.all())
    return render_template('map.html.jinja2', years=years), 404


@app.errorhandler(500)
def internal_error(e):
    flash("Un problème est survenu durant l'affichage de cette page.", "error")
    years = list(Year.query.all())
    return render_template('map.html.jinja2', years=years), 500


@app.route('/schedule/<string:year>/<string:group_name>/<string:offset>')
@app.route('/schedule/<string:year>/<string:group_name>/')
@app.route('/')
@cache.cached()
def index(year="ricm5", group_name="complet", offset=0):
    offset = int(offset)
    group = Group.query.filter_by(year_name=year, name=group_name).first()
    schedules = []
    for schedule in group.schedules:
        schedule.image = schedule.load_image_or_cache(offset)
        schedules.append(schedule)
    data = dict(title=group.title,
                offset=offset,
                schedules=schedules)

    return render_template('index.html.jinja2', **data)


@app.route('/map')
def sitemap():
    years = list(Year.query.all())
    return render_template('map.html.jinja2', years=years)


@app.route('/clear_cache')
def clear_cache():
    cache.cache.clear()
    return u'Cache purgé avec succès'


@app.route('/ical/<string:year>-group-<string:group_name>.ics')
def ical(year, group_name):
    strIO = StringIO.StringIO(get_calendar_group(year, group_name))
    strIO.seek(0)
    filename = "%s-group-%s.ics" % (year, group_name)
    return send_file(strIO, attachment_filename=filename, as_attachment=True)


@cache.memoize()
def get_calendar_group(year, group_name):
    group = Group.query.filter_by(year_name=year,
                                  name=group_name).first_or_404()
    return group.calendar.encode('utf-8')

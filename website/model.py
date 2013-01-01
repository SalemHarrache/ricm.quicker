# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from datetime import datetime, timedelta, date

import requests
from flask import url_for
from icalendar import Calendar

from .utils import get_identifier, get_schedule_events
from .extensions import db


class Site(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    host = db.Column(db.String(255))
    default_resources = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    login = db.Column(db.String(255))
    password = db.Column(db.String(255))
    order = db.Column(db.Integer)
    reference_date = db.Column(db.DateTime)

    __mapper_args__ = {'order_by': order.asc()}

    def __init__(self, name, host, default_resources, project_id, login,
                 password, reference_date, order=0):
        self.name = name
        self.host = host
        self.default_resources = default_resources
        self.project_id = project_id
        self.login = login
        self.password = password
        self.reference_date = reference_date
        self.order = order

    @property
    def auth_url(self):
        url = '%s/custom/modules/plannings/direct_planning.jsp?' \
              'projectId=%s&login=%s&password=%s&resources=%s&days=' \
              '0,1,2,3,4&displayConfId=1'
        return url % (self.host, self.project_id, self.login, self.password,
                      self.default_resources)

    @property
    def identifier(self):
        return get_identifier(self.auth_url, self.host)


class Year(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    pretty_year = db.Column(db.UnicodeText)
    pretty_field = db.Column(db.UnicodeText)

    __mapper_args__ = {'order_by': name.asc()}

    def __init__(self, name, pretty_year, pretty_field):
        self.name = name
        self.pretty_year = pretty_year
        self.pretty_field = pretty_field


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    year_name = db.Column(db.String(255), db.ForeignKey('year.name'))
    year = db.relationship('Year',
                           backref=db.backref('groups', lazy='dynamic'))

    __mapper_args__ = {'order_by': name.asc()}

    def __init__(self, year_name, name):
        self.year_name = year_name
        self.name = name

    @property
    def calendar(self):
        data = self.reload_calendar()
        item = ScheduleGroupIcal.query.filter_by(group_id=self.id).first()
        if item:
            if data:
                item.date = datetime.now()
                item.data = data
                db.session.merge(item)
                db.session.commit()
            return item.data
        else:
            if data:
                item = ScheduleGroupIcal(self.id, data, datetime.now())
                db.session.add(item)
                db.session.commit()
                return item.data

    def reload_calendar(self):
        events = []
        for schedule in self.schedules:
            events.extend(schedule.get_list_event())
        cal = Calendar()
        cal.add('prodid', '//ADEWEB Quicker//%s//FR' % self.title)
        cal.add('version', '2.0')
        for event in events:
            cal.add_component(event)
        return cal.to_ical()

    @property
    def title(self):
        return '%s Groupe %s' % (self.year_name.upper(), self.name.title())

    def next_link(self, offset):
        if offset == -1:
            href = url_for('.index', year=self.year_name, group_name=self.name)
        else:
            href = url_for('.index', year=self.year_name, offset=offset + 1,
                           group_name=self.name)
        return '<a class="nav next" href="%s"></a>' % href

    def previous_link(self, offset):
        if offset == 1:
            href = url_for('.index', year=self.year_name, group_name=self.name)
        else:
            href = url_for('.index', year=self.year_name, offset=offset - 1,
                           group_name=self.name)
        return '<a class="nav previous" href="%s"></a>' % href


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_name = db.Column(db.String(255))
    site_name = db.Column(db.String(255), db.ForeignKey('site.name'))
    site = db.relationship('Site',
                           backref=db.backref('schedules', lazy='dynamic'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group',
                            backref=db.backref('schedules', lazy='dynamic'))
    tree_id = db.Column(db.Integer)

    def __init__(self, site_name, group_id, tree_id, schedule_name=None):
        self.schedule_name = schedule_name
        self.site_name = site_name
        self.group_id = group_id
        self.tree_id = tree_id

    @property
    def week(self):
        delta = (datetime.now() + timedelta(days=3)) - self.site.reference_date
        date_year = date(self.site.reference_date.year, 1, 1)
        return (date_year + delta).isocalendar()[1] - 1

    @property
    def order(self):
        return self.site.order

    @property
    def auth_url(self):
        url = '%s/custom/modules/plannings/direct_planning.jsp?' \
              'projectId=%s&login=%s&password=%s&resources=%s&days=' \
              '0,1,2,3,4&displayConfId=1'
        return url % (self.site.host, self.site.project_id, self.site.login,
                      self.site.password, self.tree_id)

    @property
    def title(self):
        if self.schedule_name:
            return self.schedule_name
        title = u'%s - %s Groupe %s'
        year = self.group.year.name.upper()
        group_name = self.group.name.title()
        site_name = self.site.name.title()
        return title % (site_name, year, group_name)

    def url_img(self, offset):
        url = '%s/imageEt?identifier=%s&projectId=%d&idPianoWee' \
              'k=%d&idPianoDay=0%%2C1%%2C2%%2C3%%2C4&idTree=%d&' \
              'width=1200&height=800&lunchName=REPAS&displayMod' \
              'e=1057855&showLoad=false&ttl=1315827875840&displ' \
              'ayConfId=22'
        return url % (self.site.host, self.site.identifier,
                      self.site.project_id, self.week + offset, self.tree_id)

    def pretty_name(self, offset):
        pattern = "%s - %s Groupe %s - Semaine %s"
        return pattern % (self.group.year.pretty_year,
                          self.group.year.name.upper(),
                          self.group.name,
                          self.week + offset)

    def get_list_event(self):
        return get_schedule_events(self.auth_url, self.site.host,
                                   self.site.name)

    def get_image_data(self, offset):
        r = requests.get(self.url_img(offset))
        if r.status_code == requests.codes.ok:
            return r.content.encode('base64')

    def load_image_or_cache(self, offset):
        data = self.get_image_data(offset)
        item = ScheduleImage.query.filter_by(schedule_id=self.id,
                                             week=self.week + offset).first()
        if item:
            if data:
                item.date = datetime.now()
                item.data = data
                db.session.merge(item)
                db.session.commit()
            return item
        else:
            if data:
                item = ScheduleImage(self.id,
                                     self.week + offset,
                                     data, datetime.now())
                db.session.add(item)
                db.session.commit()
                return item


class ScheduleGroupIcal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group')
    data = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, group_id, data, date):
        self.group_id = group_id
        self.data = data
        self.date = date


class ScheduleImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    schedule = db.relationship('Schedule')
    week = db.Column(db.Integer)
    data = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, schedule_id, week, data, date):
        self.schedule_id = schedule_id
        self.week = week
        self.data = data
        self.date = date

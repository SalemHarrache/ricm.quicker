# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from .extensions import db
from .model import Site, Year, Group, Schedule


def init_sites():
    """Initializes sites data"""
    reference_date = datetime(2012, 8, 20)
    db.session.add(Site('Polytech', 'http://ade52-ujf.grenet.fr/ade/', 1117,
                        15, 'voirPOLYTECH', 'polytech', reference_date, 0))
    db.session.add(Site('IMAG', 'http://ade52-ujf.grenet.fr/ade/', 9, 6,
                        'voirIMA', 'ima', reference_date, 1))
    db.session.commit()


def init_years():
    """Initializes fields data"""
    pretty_field = 'Réseaux Informatiques et Communication Multimédia'
    db.session.add(Year('ricm3', u'3ème année', pretty_field))
    db.session.add(Year('ricm4', u'4ème année', pretty_field))
    db.session.add(Year('ricm5', u'5ème année', pretty_field))
    db.session.commit()


def init_groups():
    """Initializes groups data"""
    db.session.add(Group('ricm4', 'g1'))
    db.session.add(Group('ricm4', 'g2'))
    db.session.add(Group('ricm4', 'reseau'))
    db.session.add(Group('ricm4', 'multimedia'))
    db.session.add(Group('ricm4', 'complet'))

    db.session.add(Group('ricm3', 'complet'))
    db.session.add(Group('ricm3', 'g1'))
    db.session.add(Group('ricm3', 'g2'))

    db.session.add(Group('ricm5', 'complet'))
    db.session.add(Group('ricm5', 'reseau'))
    db.session.add(Group('ricm5', 'multimedia'))

    db.session.commit()


def add_schedule(year_name, group_name, site_name, tree_id,
                 schedule_name=None):
    """ Add a schedule """
    group = Group.query.filter_by(name=group_name, year_name=year_name).first()
    db.session.add(Schedule(site_name, group.id, tree_id, schedule_name))
    db.session.commit()


def init_schedules():
    """Initializes schedules data"""
    add_schedule("ricm5", 'complet', 'Polytech', 1124)
    add_schedule("ricm5", 'complet', 'IMAG', 11)
    add_schedule("ricm5", 'multimedia', 'Polytech', 1016)
    add_schedule("ricm5", 'multimedia', 'IMAG', 28)
    add_schedule("ricm5", 'reseau', 'Polytech', 1015)
    add_schedule("ricm5", 'reseau', 'IMAG', 105)

    add_schedule("ricm4", 'g1', 'Polytech', 839)
    add_schedule("ricm4", 'g1', 'IMAG', 26)
    add_schedule("ricm4", 'g2', 'Polytech', 857)
    add_schedule("ricm4", 'g2', 'IMAG', 103)
    add_schedule("ricm4", 'complet', 'Polytech', 1117)
    add_schedule("ricm4", 'complet', 'IMAG', 9)
    add_schedule("ricm4", 'multimedia', 'Polytech', 1133)
    add_schedule("ricm4", 'multimedia', 'IMAG', 103)
    add_schedule("ricm4", 'reseau', 'Polytech', 1132)
    add_schedule("ricm4", 'reseau', 'IMAG', 26)

    add_schedule("ricm3", 'complet', 'Polytech', 1110)
    add_schedule("ricm3", 'complet', 'Polytech', 1223, 'Tronc commun')
    add_schedule("ricm3", 'complet', 'IMAG', 10)
    add_schedule("ricm3", 'g1', 'Polytech', 1017)
    add_schedule("ricm3", 'g1', 'IMAG', 27)
    add_schedule("ricm3", 'g1', 'Polytech', 1223, 'Tronc commun')
    add_schedule("ricm3", 'g2', 'Polytech', 1019)
    add_schedule("ricm3", 'g2', 'IMAG', 19)
    add_schedule("ricm3", 'g2', 'Polytech', 1223, 'Tronc commun')


def init_database(*args, **kwargs):
    init_sites()
    init_years()
    init_groups()
    init_schedules()

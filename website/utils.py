# -*- coding: utf-8 -*-
'''
    :copyright: Copyright 2013 Salem Harrache.
    :license: BSD, see LICENSE for details.

'''
from __future__ import unicode_literals
import re
import uuid
import pytz
import requests

from datetime import datetime, timedelta

from icalendar import Event
from BeautifulSoup import BeautifulSoup

from .extensions import cache


@cache.memoize()
def get_identifier(auth_url, host):
    s = requests.session()
    s.get(auth_url, allow_redirects=False)
    r = s.get('%s/custom/modules/plannings/pianoWeeks.jsp?searchWeeks=all')
    r = s.get('%s/custom/modules/plannings/imagemap.jsp?width=10&he'
              'ight=10' % host, allow_redirects=False)
    try:
        return re.finditer(r"(identifier=)(.*?)(&)", r.text).next().group(2)
    except:
        pass


@cache.memoize()
def get_schedule_events(auth_url, host, location):
    s = requests.session()
    s.get(auth_url, allow_redirects=False)
    r = s.get('%s/custom/modules/plannings/pianoWeeks.jsp?searchWeeks=all' %
              host, allow_redirects=False)
    r = s.get('%s/custom/modules/plannings/info.jsp?order=slot&light=true' %
              host, allow_redirects=False)
    data = {"showTabActivity": True, "showTabDate": True, "showTabHour": True,
            "showTabDuration": True, "showImage": True, "displayConfId": 4,
            "showPianoWeeks": True, "showPianoDays": True, "display": True,
            "isClickable": True, "changeOptions": True, "displayType": 0,
            "showLoad": False, "showTree": True, "showTabTrainees": True,
            "sC": False, "sTy": False, "sUrl": False, "sE": False,
            "sM": False, "sJ": False, "sA1": False, "sA2": False,
            "sZp": False, "sCi": False, "sSt": False, "sCt": False,
            "sT": False, "sF": False, "sCx": False, "sCy": False,
            "sCz": False, "sTz": False, "showTabInstructors": True,
            "iC": False, "iTy": False, "iUrl": False, "iE": False,
            "iM": False, "iJ": False, "iA1": False, "iA2": False,
            "iZp": False, "iCi": False, "iSt": False, "iCt": False,
            "iT": False, "iF": False, "iCx": False, "iCy": False,
            "iCz": False, "iTz": False, "showTabRooms": True,
            "roC": False, "roTy": False, "roUrl": False, "roE": False,
            "roM": False, "roJ": False, "roA1": False, "roA2": False,
            "roZp": False, "roCi": False, "roSt": False, "roCt": False,
            "roT": False, "roF": False, "roCx": False, "roCy": False,
            "roCz": False, "roTz": False, "showTabResources": True,
            "reC": False, "reTy": False, "reUrl": False, "reE": False,
            "reM": False, "reJ": False, "reA1": False, "reA2": False,
            "reZp": False, "reCi": False, "reSt": False, "reCt": False,
            "reT": False, "reF": False, "reCx": False, "reCy": False,
            "reCz": False, "reTz": False, "showTabCategory5": True,
            "c5C": False, "c5Ty": False, "c5Url": False, "c5E": False,
            "c5M": False, "c5J": False, "c5A1": False, "c5A2": False,
            "c5Zp": False, "c5Ci": False, "c5St": False, "c5Ct": False,
            "c5T": False, "c5F": False, "c5Cx": False, "c5Cy": False,
            "c5Cz": False, "c5Tz": False, "showTabCategory6": True,
            "c6C": False, "c6Ty": False, "c6Url": False, "c6E": False,
            "c6M": False, "c6J": False, "c6A1": False, "c6A2": False,
            "c6Zp": False, "c6Ci": False, "c6St": False, "c6Ct": False,
            "c6T": False, "c6F": False, "c6Cx": False, "c6Cy": False,
            "c6Cz": False, "c6Tz": False, "showTabCategory7": True,
            "c7C": False, "c7Ty": False, "c7Url": False, "c7E": False,
            "c7M": False, "c7J": False, "c7A1": False, "c7A2": False,
            "c7Zp": False, "c7Ci": False, "c7St": False, "c7Ct": False,
            "c7T": False, "c7F": False, "c7Cx": False, "c7Cy": False,
            "c7Cz": False, "c7Tz": False, "showTabCategory8": True,
            "c8C": False, "c8Ty": False, "c8Url": False, "c8E": False,
            "c8M": False, "c8J": False, "c8A1": False, "c8A2": False,
            "c8Zp": False, "c8Ci": False, "c8St": False, "c8Ct": False,
            "c8T": False, "c8F": False, "c8Cx": False, "c8Cy": False,
            "c8Cz": False, "c8Tz": False}
    r = s.post('%s/custom/modules/plannings/appletparams.jsp' % host,
               data=data)
    r = s.get('%s/custom/modules/plannings/info.jsp?order=slot&light=true' %
              host, allow_redirects=False)
    items = parse_html_table(r.text, location)
    return sorted(items, key=lambda item: item["dtstart"], reverse=False)


def parse_html_table(html, location):
    def get_utc_datetime(string):
        local = pytz.timezone('Europe/Paris')
        naive = datetime.strptime(string, "%d/%m/%Y")
        local_dt = local.localize(naive, is_dst=None)
        return local_dt.astimezone(pytz.utc)

    def parse_event_id(string):
        re1 = 'javascript:ev\((\\d+)'
        rg = re.compile(re1, re.IGNORECASE | re.DOTALL)
        m = rg.search(string)
        if m:
            return m.group(1)
        else:
            return str(uuid.uuid4())

    def duration_to_date(date, string):
        if string.endswith('h'):
            string = u"%s00" % string
        else:
            string = string.replace('min', '')
        hours, minutes = 0, 0
        items = list(int(i) for i in string.split('h'))
        if len(items) == 1:
            minutes = items[0]
        elif len(items) == 2:
            hours, minutes = items[0], items[1]
        return date + timedelta(seconds=((hours) * 3600 + minutes * 60))

    soup = BeautifulSoup(html)
    table = soup.find('table')
    rows = list(table.findAll('tr'))
    if len(rows) > 2:
        for tr in rows[2:]:
            cols = [(td.find(text=True) or '') for td in tr.findAll('td')]
            date = get_utc_datetime(cols[0])
            start_date = duration_to_date(date, cols[2])
            stop_date = duration_to_date(start_date, cols[3])
            summary = cols[1]
            if cols[6]:
                classroom = cols[6]
            else:
                classroom = "Salle inconnue"
            location_title = "%s - %s" % (location, classroom)
            if cols[4]:
                summary = "%s - %s - %s" % (summary, cols[4], location_title)
            event = Event()
            event.add('summary', summary)
            event.add('dtstart', start_date)
            event.add('dtend', stop_date)
            event.add('dtstamp', date)
            event.add('location', location_title)
            event['uid'] = parse_event_id(str(tr))
            yield event

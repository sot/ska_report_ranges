# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""

Tiny utilities to work with the standard timeranges expected in
FOT reports.  These utilities change back and forth from string
specifications (e.g. "2009-Q1" for the first quarter of 2009) and
"timerange" dictionaries which are of the form

 | { 'type' : 'quarter',
 |   'start': mx.DateTime of the start time,
 |   'stop' : mx.DateTime of the stop time,
 |   'year' : 2009
 |   'subid' : 'Q1'
 | }
"""


import re
from Chandra.Time import DateTime
import calendar

month = {'Jan': 1,
         'Feb': 2,
         'Mar': 3,
         'Apr': 4,
         'May': 5,
         'Jun': 6,
         'Jul': 7,
         'Aug': 8,
         'Sep': 9,
         'Oct': 10,
         'Nov': 11,
         'Dec': 12}


def in_quarter(ref_date):

    """ which FOT quarter contains a reference date

    :param ref_date: reference date
    :rtype: range_string e.g. 2009-Q1
    """
    ref_date = DateTime(ref_date)
    for_month = {'Jan': 1,
                 'Feb': 2,
                 'Mar': 2,
                 'Apr': 2,
                 'May': 3,
                 'Jun': 3,
                 'Jul': 3,
                 'Aug': 4,
                 'Sep': 4,
                 'Oct': 4,
                 'Nov': 1,
                 'Dec': 1}

    month = calendar.month_abbr[ref_date.mon]
    if month == 'Nov' or month == 'Dec':
        year = ref_date.year + 1
    else:
        year = ref_date.year
    return "%4d-Q%d" % (year, for_month[month])


def quarter_range(year, quarter):
    """range of a FOT quarter

    :param year: integer year
    :param quarter: 1,2,3, or 4
    :rtype: timerange dictionary
    """
    quarter_starts = {1: 'Nov',
                      2: 'Feb',
                      3: 'May',
                      4: 'Aug'}

    quarter_stops = {1: 'Feb',
                     2: 'May',
                     3: 'Aug',
                     4: 'Nov'}

    month_start = month[quarter_starts[quarter]]
    if month_start == 11:
        year_start = year - 1
    else:
        year_start = year
    month_stop = month[quarter_stops[quarter]]
    year_stop = year
    start = DateTime("{:04d}-{:02d}-01 00:00:00.000".format(year_start, month_start))
    stop = DateTime("{:04d}-{:02d}-01 00:00:00.000".format(year_stop, month_stop))
    return {'type': 'quarter',
            'start': start,
            'stop': stop,
            'year': year,
            'subid': 'Q%d' % quarter}


def in_semi(ref_date):
    """ which FOT half-year contains a reference date

    :param ref_date: mx.DateTime reference date
    :rtype: range_string e.g. 2009-S1
    """
    ref_date = DateTime(ref_date)
    for_month = {'Jan': 1,
                 'Feb': 2,
                 'Mar': 2,
                 'Apr': 2,
                 'May': 2,
                 'Jun': 2,
                 'Jul': 2,
                 'Aug': 1,
                 'Sep': 1,
                 'Oct': 1,
                 'Nov': 1,
                 'Dec': 1}

    month = calendar.month_abbr[ref_date.mon]
    if (ref_date.mon >= 2 and ref_date.mon < 8) or month == 'Jan':
        year = ref_date.year
    else:
        year = ref_date.year + 1
    return "%4d-S%d" % (year, for_month[month])


def semi_range(year, semi):
    """range of a FOT half-year

    :param year: integer year
    :param semi: 1,2
    :rtype: timerange dictionary
    """
    semi_starts = {1: 'Aug',
                   2: 'Feb'}

    semi_stops = {1: 'Feb',
                  2: 'Aug'}

    month_start = month[semi_starts[semi]]
    if month_start < 8:
        year_start = year
    else:
        year_start = year - 1
    month_stop = month[semi_stops[semi]]
    year_stop = year
    start = DateTime("{:04d}-{:02d}-01 00:00:00.000".format(year_start, month_start))
    stop = DateTime("{:04d}-{:02d}-01 00:00:00.000".format(year_stop, month_stop))
    return {'type': 'semi',
            'start': start,
            'stop': stop,
            'year': year,
            'subid': 'S%d' % semi}


def in_year(ref_date):
    """ which year contains a reference date

    :param ref_date: mx.DateTime reference date
    :rtype: range_string e.g. '2010'
    """
    ref_date = DateTime(ref_date)
    return "%4d" % ref_date.year


def year_range(year):
    """find year start, stop

    :param year: int year
    :rtype: timerange dictionary
    """
    return {'type': 'year',
            'start': DateTime("{:04d}-01-01 00:00:00.000".format(int(year))),
            'stop': DateTime("{:04d}-01-01 00:00:00.000".format(int(year) + 1)),
            'year': year,
            'subid': 'YEAR'}


def in_month(ref_date):
    """ which month contains a reference date

    :param ref_date: mx.DateTime reference date
    :rtype: range_string e.g. 2007-M12
    """
    return "%4d-M%02d" % (ref_date.year, ref_date.mon)


def month_range(year, month):
    """
    month range

    :param year: year
    :param month: integer month
    :rtype: timerange dictionary
    """
    month_stop = month + 1
    year_stop = year
    if month_stop == 13:
        year_stop = year + 1
        month_stop = 1

    return {'type': 'month',
            'start': DateTime("{:04d}-{:02d}-01 00:00:00.000".format(year, month)),
            'stop': DateTime("{:04d}-{:02d}-01 00:00:00.000".format(year_stop, month_stop)),
            'year': year,
            'subid': 'M%02d' % month}


def in_range(range_type, ref_date):
    ref_date = DateTime(ref_date)
    if range_type == 'month':
        return in_month(ref_date)
    if range_type == 'quarter':
        return in_quarter(ref_date)
    if range_type == 'semi':
        return in_semi(ref_date)
    if range_type == 'year':
        return in_year(ref_date)
    raise ValueError("unexpected range_type, not 'month', 'quarter', 'semi', or 'year'")


def timerange(rstring):
    """
    range from string specifier

    |  2010-M08 -> range of August 2010
    |  2009-Q1 -> range of first quarter, 2009
    |  2001-S1 -> range of first "semi" 2001
    |  2008 -> range of year 2008

    :param rstring: range string
    :rtype: timerange dictionary
    """
    m_match = re.search(r'(\d{4})-M(\d{2})', rstring)
    if m_match:
        return month_range(int(m_match.group(1)), int(m_match.group(2)))
    q_match = re.search(r'(\d{4})-Q(\d{1})', rstring)
    if q_match:
        return quarter_range(int(q_match.group(1)), int(q_match.group(2)))
    s_match = re.search(r'(\d{4})-S(\d{1})', rstring)
    if s_match:
        return semi_range(int(s_match.group(1)), int(s_match.group(2)))
    y_match = re.search(r'(\d{4})', rstring)
    if y_match:
        return year_range(int(y_match.group(1)))


def get_update_ranges(days=365):
    """
    Find all of the day ranges from now-N days to now.

    :param days: N days back as starting point
    :rtype: dict of labeled day ranges
    """
    now = DateTime()
    times = {}
    # works by performing the "in_range" operation on each day,
    # hence the walk through using range
    for day_back in range(0, days):
        then = now - day_back
        for range_type in ('month', 'quarter', 'semi', 'year'):
            time_str = in_range(range_type, then)
            if time_str not in times:
                times[time_str] = timerange(time_str)
    return times


def get_prev(range):
    """
    Find the time range before the given one

    :param range: timerange dictionary
    :rtype: timerange dictionary

    """
    ref_time = DateTime(range['start'].secs - 1)
    old_range = in_range(range['type'], ref_time)
    return timerange(old_range)


def get_next(range):
    """
    Find the time range after the given one

    :param range: timerange dictionary
    :rtype: timerange dictionary

    """
    ref_time = range['stop']
    next_range = in_range(range['type'], ref_time)
    return timerange(next_range)

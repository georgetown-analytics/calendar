# gtcal.utils
# Utility functions for calendar app
#
# Author:  Benjamin Bengfort <bb830@georgetown.edu>
# Created: Thu Mar 27 21:34:59 2014 -0400
#
# Copyright (C) 2014 Georgetown University
# For license information, see LICENSE.txt
#
# ID: utils.py [] bb830@georgetown.edu $

"""
Utility functions for calendar app
"""

##########################################################################
## Imports
##########################################################################

import json

from datetime import datetime

##########################################################################
## Date and Time representations
##########################################################################

## Format dates and times as strings
SHORT_DATE    = "%Y-%m-%d"
LONG_DATE     = "%B %d, %Y"
TIME_FORMAT   = "%I:%M %p"
LONG_DATETIME = "%B %d, %Y at %I:%M %p"
JSON_FORMAT   = "%Y-%m-%dT%H:%M:%S.%fz"

##########################################################################
## Console Helpers
##########################################################################

def parse_date(dstr):
    """
    Attempts to parse the datetime from a string
    """

    def parse(dstr, dfmt):
        try:
            return datetime.strptime(dstr, dfmt)
        except ValueError:
            return None

    dates = ("%m/%d/%Y", "%Y-%m-%d")
    times = ("%H:%M", "%H:%M:%S", "%I:%M %p")

    for datefmt in dates:
        # Try every date format
        dt = parse(dstr, datefmt)
        if dt is not None:
            return dt

        # Try every combination of dates and times
        for timefmt in times:
            dt = parse(dstr, datefmt + " " + timefmt)
            if dt is not None:
                return dt

    # Try every time format
    for timefmt in times:
        dt = parse(dstr, timefmt)
        if dt is not None:
            # Ok, so this is implied today, need to deal with that
            today = datetime.today()
            return dt.replace(year=today.year, month=today.month, day=today.day)

    return None

##########################################################################
## Helpers for Serializing/Deserializing JSON data
##########################################################################

class CalendarEncoder(json.JSONEncoder):
    """
    Custom encoder that handles datetimes.
    """

    def default(self, obj):

        # Check if the object is a datetime
        if isinstance(obj, datetime):
            # Return the string representation of the date
            return obj.strftime(JSON_FORMAT)

        # Check if the object has a serialize method
        if hasattr(obj, 'serialize'):
            # Return a dictionary of the event data
            return obj.serialize()

        # Otherwise just do the default behavior
        return super(CalendarEncoder, self).default(obj)


class CalendarDecoder(json.JSONDecoder):
    """
    Custom encoder that handles datetimes.
    """

    def decode(self, s):
        try:
            # Attempt to return the datetime from the data
            return datetime.strptime(s, JSON_FORMAT)
        except ValueError:
            return super(CalendarDecoder, self).decode(s)

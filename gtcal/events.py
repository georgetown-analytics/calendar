# gtcal.events
# Events class hierarchy
#
# Author:  Benjamin Bengfort <bb830@georgetown.edu>
# Created: Mon Sep 14 19:17:10 2015 -0400
#
# Copyright (C) 2014 Georgetown University
# For license information, see LICENSE.txt
#
# ID: events.py [] bb830@georgetown.edu $

"""
Events class hierarchy
"""

##########################################################################
## Imports
##########################################################################

from datetime import datetime, timedelta
from gtcal.utils import LONG_DATETIME, SHORT_DATE

##########################################################################
## Event Classes
##########################################################################

class Event(object):
    """
    Base event class that contains all properties and behavior of events.
    """

    def __init__(self, name, start, end, notes=None, location=None):
        self.name  = name
        self.start = start
        self.end   = end
        self.notes = notes
        self.location = location

    @property
    def key(self):
        """
        Returns the key to store this event in storage, based on the start.
        """
        return self.start.strftime(SHORT_DATE)

    def duration(self):
        """
        Calculates how long the event will be in hours.
        """
        delta = self.end - self.start # This returns a time delta object

        # If event is multiple days, return number of days
        if delta.days > 0:
            return "%i days" % delta.days

        # Attempt to report delta in meaningful time unit (hours, minutes)
        if delta.seconds >= 3600:
            hours = delta.seconds / 3600.0
            return "%0.2f hours" % hours
        else:
            minutes = delta.seconds / 60
            return "%i minutes" % minutes

    def pprint(self, short=False):
        """
        Print an event with all it's details. If short, only print a simple
        description, not all the details of the event.
        """
        if short:
            # Simplest, shortest representation
            return "%s on %s" % (self.name, self.start.strftime(LONG_DATETIME))

        # Otherwise put together a longer print out.
        output = []
        output.append(self.name)
        output.append("from %s to %s" % (self.start.strftime(LONG_DATETIME), self.end.strftime(LONG_DATETIME)))
        output.append("(%s)" % self.duration())

        if self.location:
            output.append("at %s" % self.location)

        if self.notes:
            output.append("")
            output.append("Notes:")
            output.append(self.notes)

        return "\n".join(output)

    def serialize(self):
        return {
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "notes": self.notes,
            "location": self.location
        }

    def __str__(self):
        return self.pprint(short=True)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.pprint(short=True))

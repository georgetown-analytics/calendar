# gtcal.calendar
# Calendar keeps track of events and loads information from disk.
#
# Author:   Benjamin Bengfort <bb830@georgetown.edu>
# Created:  Mon Sep 14 19:17:10 2015 -0400
#
# Copyright (C) 2015 Georgetown University
# For license information, see LICENSE.txt
#
# ID: calendar.py [] benjamin@bengfort.com $

"""
Calendar keeps track of events and loads information from disk.
"""

##########################################################################
## Imports
##########################################################################

import os
import json

from datetime import datetime
from collections import defaultdict

from gtcal.events import Event
from gtcal.utils import SHORT_DATE
from gtcal.utils import CalendarEncoder, CalendarDecoder

##########################################################################
## Main Calendar App
##########################################################################

class Calendar(object):
    """
    A calender holds and manages events, saving and loading them to disk.
    """

    def __init__(self, path=None):
        # Storage is a dictionary of date --> list of events
        self.storage  = defaultdict(list)
        self.location = path

    def load(self):
        """
        Load data from path and store in memory.

        Note that load checks if the data exists, otherwise it does nothing,
        refusing to raise an exception.
        """
        # Get the path and check if it exists
        if not os.path.exists(self.location): return

        # Open the path for reading
        with open(self.location, 'r') as data:
            # load the data from disk
            data = json.load(data, cls=CalendarDecoder)

            # parse the data into events
            for key, values in data.iteritems():
                for value in values:
                    self.add_event(**value)

    def save(self):
        """
        Save the calendar from memory back to disk.
        """
        # Open the file for writing
        with open(self.location, 'w') as f:
            # Dump the data to the file
            json.dump(self.storage, f, indent=2, cls=CalendarEncoder)

    def add_event(self, **kwargs):
        """
        Adds an event by creating the event with the arbitrary list of
        arguments that is passed into this method, then stores it according
        to the year and the day in our internal storage.
        """
        event = Event(**kwargs)                  # Create event
        self.storage[event.key].append(event)    # Store the event
        return event

    def todays_agenda(self):
        """
        Creates a nice print out of the agenda for today
        """
        today  = datetime.today()                           # What day is today?
        events = self.storage[today.strftime(SHORT_DATE)]   # Get the events out of storage

        # Check if we have anything
        if not events:
            return "No events scheduled for today!"

        # Otherwise, start creating agenda
        output = []

        # Create a nice agenda header
        output.append("Agenda for %s:" % today.strftime("%B %d, %Y"))
        output.append("    You have %i events" % len(events))
        output.append("=" * len(output[0]))
        output.append("") # This will create a blank line

        for event in events:
            output.append(event.pprint(date_format="%I:%M %p"))
            output.append("-" * len(output[0]))
            output.append("") # This will create a blank line

        return "\n".join(output)

    def __len__(self):
        numevents = 0
        for date in self.storage:
            numevents += len(self.storage[date])
        return numevents

    def __str__(self):
        output = str(self.__class__.__name__)
        if self.location:
            output += " at %s" % self.location
        output += " with %i events" % (len(self))
        return output

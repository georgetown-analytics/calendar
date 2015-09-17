# tests.test_gtcal
# Tests the calendar functionality from end to end.
#
# Author:   Benjamin Bengfort <bb830@georgetown.edu>
# Created:  Thu Sep 17 13:57:31 2015 -0400
#
# Copyright (C) 2015 Georgetown University
# For license information, see LICENSE.txt
#
# ID: test_gtcal.py [] benjamin@bengfort.com $

"""
Tests the calendar functionality from end to end.
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest

from datetime import datetime

from gtcal.calendar import Calendar
from gtcal.events import Event

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "fixtures", "test_calendar.json")

##########################################################################
## Calendar Testing
##########################################################################

class CalendarTests(unittest.TestCase):

    def tearDown(self):
        """
        Make sure test calendar is removed.
        """
        if os.path.exists(FIXTURE):
            os.unlink(FIXTURE)

    def test_calendar(self):
        """
        Test loading an empty calendar, adding events, saving, and loading.
        """

        calendar = Calendar(FIXTURE)
        calendar.load()

        self.assertEqual(len(calendar), 0)

        e1 = {'name': 'Test Event 1', 'start': datetime(2015, 04, 07, 13), 'end': datetime(2015, 04, 07, 14, 30)}
        e2 = {'name': 'Test Event 2', 'start': datetime(2015, 04, 07, 15), 'end': datetime(2015, 04, 07, 15, 30)}

        calendar.add_event(**e1)
        calendar.add_event(**e2)

        self.assertEqual(len(calendar), 2)
        calendar.save()
        return

        tcal = Calendar(FIXTURE)
        tcal.load()
        self.assertEqual(len(tcal), 2)

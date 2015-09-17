#!/usr/bin/env python
# calendar
# The command line program for user interaction with gtcal.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Sep 14 20:15:06 2015 -0400
#
# Copyright (C) 2015 Georgetown University
# For license information, see LICENSE.txt
#
# ID: calendar.py [] benjamin@bengfort.com $

"""
The command line program for user interaction with gtcal.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import gtcal
import argparse

from gtcal import Calendar
from gtcal import parse_date

##########################################################################
## Script Definition
##########################################################################

# Store calendar data in fixtures directory, relative to this file.
CALENDAR = os.path.join(os.path.dirname(__file__), "fixtures", "calendar.json")

# Describe the app to the user.
VERSION  = gtcal.__version__
DESCRIPTION = "The Georgetown calendar management console application."
EPILOG   = "Please report any bugs or issues on Github."

##########################################################################
## Command line helpers
##########################################################################

def parse_input(prompt, parse, message):
    """
    Parses input (like dates and times) from input on the command line.
    """
    value = raw_input(prompt)
    value = parse(value)

    if value is None:
        print message
        return parse_input(prompt, parse, message)

    return value

##########################################################################
## Commands
##########################################################################

def add(args):
    """
    Add an event to the calendar.
    """
    # Create and load the calendar
    calendar = Calendar(CALENDAR)
    calendar.load()

    name     = parse_input("name: ", lambda x: x if x else None, "Please provide an event name!")
    start    = parse_input("start: ", parse_date, "Specify dates as %Y-%d-%m %H:%M")
    end      = parse_input("end: ", parse_date, "Specify dates as %Y-%d-%m %H:%M")
    location = parse_input("location: ", lambda x: x, "")
    notes    = parse_input("notes: ", lambda x: x, "")

    event = calendar.add_event(name=name, start=start, end=end, notes=notes, location=location)
    calendar.save()
    print event.pprint()


def remove(args):
    """
    Remove an event from the calendar.
    """
    raise NotImplementedError("Not implemented in this solution!")


def view(args):
    """
    View the details of a single event.
    """
    raise NotImplementedError("Not implemented in this solution!")


def agenda(args):
    """
    Print today's agenda and exit.
    """
    # Create and load the calendar
    calendar = Calendar(CALENDAR)
    calendar.load()
    print calendar.todays_agenda()

##########################################################################
## Main method
##########################################################################

def main(*argv):

    # Construct the argument parser
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG, version=VERSION)
    subparsers = parser.add_subparsers(title='commands', description='Calendar commands')

    # Add Event Command
    add_cmd = subparsers.add_parser('add', help='Add an event to the calendar.')
    add_cmd.set_defaults(func=add)

    # Remove Event Command
    remove_cmd = subparsers.add_parser('remove', help='Remove an event from the calendar.')
    remove_cmd.set_defaults(func=remove)

    # View Event Command
    view_cmd = subparsers.add_parser('view', help='View the details of a single event.')
    view_cmd.set_defaults(func=view)

    # Agenda Command
    agenda_cmd = subparsers.add_parser('agenda', help='Print today\'s agenda and exit.')
    agenda_cmd.set_defaults(func=agenda)


    # Handle input from the command line
    args = parser.parse_args()            # Parse the arguments
    # try:
    msg = args.func(args)             # Call the default function
    parser.exit(0, msg+"\n")               # Exit cleanly with message
    # except Exception as e:
    #     parser.error(str(e))              # Exit with error

if __name__ == '__main__':
    main(*sys.argv)

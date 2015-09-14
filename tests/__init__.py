# tests
# Testing module for the Georgetown Calendar application
#
# Author:   Benjamin Bengfort <benjamin.bengfort@georgetown.edu>
# Author:   NAME <EMAIL>
# Created:  Mon Sep 14 19:18:16 2015 -0400
#
# Copyright (C) 2015 Georgetown University
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin.bengfort@georgetown.edu $

"""
Testing module for the Georgetown Calendar application
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Initialization Tests
##########################################################################

class InitializationTests(unittest.TestCase):
    """
    Initial tests to make sure that our test harness is working.
    """

    def test_sanity(self):
        """
        Check the world is sane and 2+2=4
        """
        self.assertEqual(2+2, 4)

    def test_import(self):
        """
        Assert that we can import the gtcal library
        """

        # TODO: Fill in this method stub!
        self.fail("Test hasn't been implemented yet!")

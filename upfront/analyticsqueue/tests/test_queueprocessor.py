import os
import csv
from cStringIO import StringIO
import unittest

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.ptc import PloneTestCase
from upfront.analyticsqueue.tests.layer import Layer

dirname = os.path.dirname(__file__)

class TestQueueProcessor(PloneTestCase):
    
    layer = Layer
    
    def test_queue_config(self):
        self.fail()

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

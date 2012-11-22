import unittest

from upfront.analyticsqueue.entities import CountProcessor

class TestCountProcessor(unittest.TestCase):

    def test_process(self):
        processor = CountProcessor()
        history = {}
        count = 0
        newcount = processor.process(count, **history)
        self.assertEqual(newcount, count +1)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

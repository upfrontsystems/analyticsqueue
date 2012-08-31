from datetime import datetime

from pyga.requests import Tracker, Page, Session

from upfront.analyticsqueue.entities import Visitor


class GoogleQueue(object):

    @classmethod
    def deliver(cls, entry):
        now = datetime.utcnow()

        # make the call to google analytics
        tracker = Tracker(entry['gacode'], entry['domain'])

        visitor = Visitor(entry)
        # possible other data:
        #visitor.flash_version = None
        #visitor.java_enabled = None
        #visitor.screen_colour_depth = None
        #visitor.screen_resolution = None

        session = Session()

        page = Page(entry['path'])
        page.referer = entry['referer'] 
        page.title = entry['title']
        #page.charset = entry['charset']
        #page.load_time = entry['load_time']

        tracker.track_pageview(page, session, visitor)

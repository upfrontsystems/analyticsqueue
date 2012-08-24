from datetime import datetime

from pyga.requests import Tracker, Page, Session, Visitor


class GoogleQueue(object):

    @classmethod
    def deliver(cls, entry):
        now = datetime.utcnow()

        # make the call to google analytics
        tracker = Tracker(entry['gacode'], entry['domain'])

        visitor = Visitor()
        visitor.current_visit_time = now
        visitor.ip_address = entry['remote_address'] 
        visitor.user_agent = entry['user_agent']
        visitor.locale = entry['locale']
        visitor.unique_id = entry['unique_id']
        # possible other data:
        #visitor.first_visit_time = now
        #visitor.previous_visit_time = now
        #visitor.visit_count = 1
        #visitor.flash_version = None
        #visitor.java_enabled = None
        #visitor.screen_colour_depth = None
        #visitor.screen_resolution = None

        session = Session()

        # drop the science or maths from the path
        path_elements = ('',) + entry['path'][2:]
        page = Page('/'.join(path_elements))
        page.referer = entry['referer'] 
        page.title = entry['title']
        #page.charset = entry['charset']
        #page.load_time = entry['']

        tracker.track_pageview(page, session, visitor)

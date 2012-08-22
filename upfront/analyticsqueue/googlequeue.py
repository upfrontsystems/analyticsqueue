from pyga.requests import Tracker, Page, Session, Visitor


class GoogleQueue(object):

    @classmethod
    def deliver(cls, entry):
        # make the call to google analytics
        tracker = Tracker(entry['gacode'], entry['domain'])
        visitor = Visitor()
        visitor.ip_address = entry['ip_address'] 
        session = Session()
        # drop the science or maths from the path
        path_elements = ('',) + entry['path'][2:]
        page = Page('/'.join(path_elements))
        tracker.track_pageview(page, session, visitor)

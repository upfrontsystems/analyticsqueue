from zope.interface import Interface


class IMobileTrackingEvent(Interface):
    """ Possible fields: 
        - unique_id
        - first_visit_time
        - previous_visit_time
        - current_visit_time
        - visit_count
        - ip_address
        - user_agent
        - locale
        - flash_version
        - java_enabled
        - screen_colour_depth
        - screen_resolution
    """

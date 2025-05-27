import requests
from wc_gc.config import (
    WCGC_BASE_URL,
    WCGC_BOOKING_PAGE_ENDPOINT,
    WCGC_CONSENT_ENDPOINT,
)


# Class to handle login and authentication
class WCGCAuth:
    def __init__(self, session: requests.Session):
        self.session = session
        self.login_url = "https://www.westcoastgolfclub.com.au/member/login"


# Class to handle the interpreting of target tee times
class TeeTimes:
    pass


# Class to handle the booking functionality
class BookingSystem:
    pass

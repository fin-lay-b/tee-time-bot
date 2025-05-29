import requests
import logging

from wc_gc.config import (
    WCGC_BASE_URL,
    WCGC_LOGOUT_ENDPOINT,
    WCGC_BOOKING_PAGE_ENDPOINT,
    WCGC_CONSENT_ENDPOINT,
)

logging.basicConfig(level=logging.INFO)
# inject session
# session = requests.Session()
# session.verify = ...


# Class to handle login and authentication
class WCSession:
    def __init__(self, memberid: str, pin: str):
        self.memberid = memberid
        self.pin = pin
        self.session = requests.Session()


    def login(self):
        try:
            login_response = self.session.post(
                WCGC_BASE_URL,
                data={"memberid": self.memberid, "pin": self.pin},
            )
            login_response.raise_for_status()

            return login_response

        except requests.exceptions.RequestException as e:
            logging.error(f"[login] Failed: {e}", exc_info=True)
            return None
            
    def logout(self):
        try:
            logout_response = self.session.get(WCGC_BASE_URL + WCGC_LOGOUT_ENDPOINT)
            logout_response.raise_for_status()

            return logout_response
        except requests.exceptions.RequestException as e:
            logging.error(f"[logout] Failed: {e}", exc_info=True)
            return None

+
    def load_booking_page(self):
        try:
            booking_page_response = self.session.get(self.booking_page_url)
            booking_page_response.raise_for_status()

            conduct_response = self.session.get(self.consent_url, allow_redirects=True)
            conduct_response.raise_for_status()

            return conduct_response

        except requests.exceptions.RequestException as e:
            logging.error(f"[load_booking_page] Failed: {e}", exc_info=True)
            return None

    def verify_login(self):
        # Check the reponse for successful login
        pass


# Class to handle the interpreting of target tee times
class TeeTimeManager:
    # Need to be ablet to check availability of tee times (competiions etc.)
    # Take target time for day of week
    # Take target time for specific date
    # Book best time in range of times
    pass


# Class to handle the booking functionality
class TeeTimeBooker:
    def __init__(self, session: requests.Session, booking_date: str, booking_time: str):
        self.session = session
        self.booking_date = booking_date
        self.booking_time = booking_time

    pass

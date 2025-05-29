import requests
from wc_gc.config import (
    WCGC_BASE_URL,
    WCGC_BOOKING_PAGE_ENDPOINT,
    WCGC_CONSENT_ENDPOINT,
)

# inject session
# session = requests.Session()
# session.verify = ...


# Class to handle login and authentication
class WCLogin:
    def __init__(self, session: requests.Session):
        self.session = session
        self.login_url = f"{WCGC_BASE_URL}"
        self.booking_page_url = f"{WCGC_BASE_URL}{WCGC_BOOKING_PAGE_ENDPOINT}"
        self.consent_url = f"{WCGC_BASE_URL}{WCGC_CONSENT_ENDPOINT}"

    def login(self, memberid: str, pin: str):
        try:
            login_response = self.session.post(
                self.login_url,
                data={"memberid": memberid, "pin": pin},
            )
            login_response.raise_for_status()

            return login_response

        except requests.exceptions.RequestException as e:
            print(f"[login] Failed: {e}")

    def load_booking_page(self):
        try:
            # Load the booking page
            booking_page_response = self.session.get(self.booking_page_url)
            # Check for errors in the booking page response
            booking_page_response.raise_for_status()

            # Accept conduct terms to proceed to booking page
            conduct_response = self.session.get(self.consent_url, allow_redirects=True)
            # Check for errors in the conduct response
            conduct_response.raise_for_status()

            return conduct_response

        except requests.exceptions.RequestException as e:
            print(f"[load_booking_page] Failed: {e}")

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

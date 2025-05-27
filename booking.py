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
class WCGCAuth:
    def __init__(self, session: requests.Session):
        self.session = session
        self.login_url = f"{WCGC_BASE_URL}"

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

    def verify_login(self):
        # Check the reponse for successful login
        pass


# Class to handle the interpreting of target tee times
class TeeTimes:
    pass


# Class to handle the booking functionality
class BookingSystem:
    pass

import requests
from typing import Optional
from pydantic import BaseModel


class BookingConfig(BaseModel):
    member_id: str
    member_pin: str
    login_url: str
    certificate_path: str
    booking_url: str
    conduct_form_url: str


class BookingSession:
    def __init__(self, config: BookingConfig):
        self.member_id: str = config.member_id
        self.member_pin: str = config.member_pin
        self.login_url: str = config.login_url
        self.certificate_path: str = config.certificate_path
        self.booking_url: str = config.booking_url
        self.conduct_form_url: str = config.conduct_form_url
        self._session: Optional[requests.Session] = None

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def login(self):
        login_data = {"memberid": self.member_id, "pin": self.member_pin}
        login_response = self.session.post(
            self.login_url, data=login_data, verify=self.certificate_path
        )

        if login_response.ok:
            print("✅ Login successful.")
            return True
        else:
            print("❌ Login failed.")
            return False

    def nav_to_booking(self):
        booking_response = self.session.get(
            self.booking_url, verify=self.certificate_path
        )

        if not booking_response.ok:
            print("❌ Booking page loading failed.")
            return False

        if "code of conduct" in booking_response.text.lower():
            print("⚠️ Code of Conduct page detected! Accepting...")

            conduct_response = self.session.get(
                self.conduct_form_url,
                verify=self.certificate_path,
                allow_redirects=True,
            )

            if not conduct_response.ok:
                print("❌ Code of Conduct acceptance failed.")
                return False

            print("✅ Code of Conduct accepted!")

            final_booking_response = self.session.get(
                self.booking_url, verify=self.certificate_path
            )
            if not final_booking_response.ok:
                print("❌ Booking page loading failed.")
                return False

            print("✅ Booking page loaded successfully.")
            return final_booking_response

        print("✅ No Code of Conduct required, booking page loaded successfully.")

        return final_booking_response

    def load_booking_page(self):
        if not self.login():
            print("❌ Login failed.")
            return False
        return self.nav_to_booking()

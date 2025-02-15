from pydantic import BaseModel, Field
import requests


# Can add more validation restraint to the fields
class BookingConfig(BaseModel):
    member_id: str = Field(..., description="Member ID for golf club")
    member_pin: str = Field(..., description="PIN for golf club")
    login_url: str = Field(..., description="URL for login page")
    certificate_path: str = Field(..., description="Path to certificate")
    booking_url: str = Field(..., description="URL for booking page")
    conduct_form_url: str = Field(..., description="URL for code of conduct form")


# To add:
# Timeout if login takes too long
class BookingSession:
    """
    Gets to right session using requests for booking a tee time.

    Args:
        ...
    Returns:
        requests.session object
    """

    def __init__(self, config: BookingConfig):
        self.config = config
        self._session: requests.Session = None

    # Remove property and initialise in __init__?
    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def login(self):
        login_data = {"memberid": self.config.member_id, "pin": self.config.member_pin}
        login_response = self.session.post(
            self.config.login_url, data=login_data, verify=self.config.certificate_path
        )

        if login_response.ok:
            print("✅ Login successful.")
            return True
        else:
            print("❌ Login failed.")
            return False

    def nav_to_booking(self):
        booking_response = self.session.get(
            self.config.booking_url, verify=self.config.certificate_path
        )

        if not booking_response.ok:
            print("❌ Booking page loading failed.")
            return False

        if "code of conduct" in booking_response.text.lower():
            print("⚠️ Code of Conduct page detected! Accepting...")

            conduct_response = self.session.get(
                self.config.conduct_form_url,
                verify=self.config.certificate_path,
                allow_redirects=True,
            )

            if not conduct_response.ok:
                print("❌ Code of Conduct acceptance failed.")
                return False

            print("✅ Code of Conduct accepted!")

            final_booking_response = self.session.get(
                self.config.booking_url, verify=self.config.certificate_path
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

import os
from dotenv import load_dotenv

from whitecraigs.access2 import BookingConfig

# Set constants for login details
# Do I want to share this publicly? Probably not


# Load environment variables
load_dotenv()
MEMBER_ID = os.getenv("GOLF_MEMBER_ID")
MEMBER_PIN = os.getenv("GOLF_PIN")
LOGIN_URL = os.getenv("LOGIN_URL")
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH")
BOOKING_URL = os.getenv("BOOKING_URL")
CONDUCT_FORM_URL = os.getenv("CONDUCT_FORM_URL")

# Create config object for booking to ensure data type is valid
config = BookingConfig(
    member_id=MEMBER_ID,
    member_pin=MEMBER_PIN,
    login_url=LOGIN_URL,
    certificate_path=CERTIFICATE_PATH,
    booking_url=BOOKING_URL,
    conduct_form_url=CONDUCT_FORM_URL,
)

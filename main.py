import os
from datetime import time

from dotenv import load_dotenv

from whitecraigs.schemas import LoginConfig
from whitecraigs.access2 import LoginSession
from whitecraigs.booking2 import TeeTimeBooker

# from whitecraigs.booking2 import TeeTimeBooker

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
config = LoginConfig(
    member_id=MEMBER_ID,
    member_pin=MEMBER_PIN,
    login_url=LOGIN_URL,
    certificate_path=CERTIFICATE_PATH,
    booking_url=BOOKING_URL,
    conduct_form_url=CONDUCT_FORM_URL,
)

# Create session object for booking
session = LoginSession(config).load_booking_page()

# Book a tee time
# TeeTimeBooker(session, tee_time)

booking_config = {
    "schedule": {
        "Monday": [
            {"start": "06:00", "end": "06:45", "range_orient": "earliest"},
            {"start": "18:00", "end": "19:00", "range_orient": "earliest"},
        ],
        "Tuesday": [
            {"start": "06:00", "end": "07:30", "range_orient": "earliest"},
        ],
        "Wednesday": [
            {"start": "16:00", "end": "17:30", "range_orient": "earliest"},
        ],
        "Thursday": [
            {"start": "16:00", "end": "17:30", "range_orient": "earliest"},
        ],
        "Friday": [
            {"start": "16:00", "end": "17:30", "range_orient": "earliest"},
        ],
        "Saturday": [
            {"start": "07:00", "end": "08:30", "range_orient": "latest"},
        ],
        "Sunday": [
            {"start": "07:00", "end": "08:30", "range_orient": "earliest"},
        ],
    }
}

tee_time = TeeTimeBooker(session, booking_config, CERTIFICATE_PATH)

print(tee_time.all_tee_times)
print(tee_time._booking_pattern)

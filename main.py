import os

from dotenv import load_dotenv

from wc_gc.schemas import LoginConfig
from wc_gc.booking import BookingSystem

load_dotenv()
MEMBER_ID = os.getenv("GOLF_MEMBER_ID")
MEMBER_PIN = os.getenv("GOLF_PIN")
BASE_URL = os.getenv("BASE_URL")
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH")
BOOKING_SCHEDULE = {
    "Monday": [],
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [],
    "Friday": [],
    "Saturday": ["08:00", "10:15"],
    "Sunday": ["08:00"],
}

config = LoginConfig(
    member_id=MEMBER_ID,
    member_pin=MEMBER_PIN,
    base_url=BASE_URL,
    certificate_path=CERTIFICATE_PATH,
    schedule=BOOKING_SCHEDULE,
)


booking_system = BookingSystem(config)

if booking_system.login():
    booking_system.load_booking_page()
    booking_system.book_tee_time()

booking_system.close_session()

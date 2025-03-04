import os
import json
import logging

from aws.tools import get_cert_value, create_cert_path, get_schedule
from wc_gc.schemas import LoginConfig
from wc_gc.booking import BookingSystem

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:

        CERTIFICATE_ARN = os.getenv("CERT_ARN")
        cert_value = get_cert_value(CERTIFICATE_ARN)
        CERTIFICATE_PATH = create_cert_path(cert_value)

        # os.environ["AWS_CA_BUNDLE"] =

        MEMBER_ID = os.getenv("GOLF_MEMBER_ID")
        MEMBER_PIN = os.getenv("GOLF_PIN")
        BASE_URL = os.getenv("BASE_URL")
        SCHEDULE_ARN = os.getenv("SCHEDULE_ARN")

        BOOKING_SCHEDULE = get_schedule(SCHEDULE_ARN)

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

        return {"statusCode": 200, "message": "Tee time booked successfully"}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "message": f"Error: {str(e)}"}),
        }

import os
import json

from aws.tools import get_cert_value, create_cert_path, get_schedule
from wc_gc.schemas import LoginConfig
from wc_gc.booking import BookingSystem


def lambda_handler(event, context):
    try:
        # Set certificate path at the beginning
        cert_path = os.path.join(os.environ.get("LAMBDA_TASK_ROOT", ""), "cert.crt")

        # Configure AWS SDK to use the certificate
        os.environ["AWS_CA_BUNDLE"] = cert_path

        MEMBER_ID = os.getenv("GOLF_MEMBER_ID")
        MEMBER_PIN = os.getenv("GOLF_PIN")
        BASE_URL = os.getenv("BASE_URL")
        SCHEDULE_ARN = os.getenv("SCHEDULE_ARN")

        CERTIFICATE_PATH = cert_path

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

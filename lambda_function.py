import os
import json
import logging
from datetime import datetime, timedelta
import time
import urllib3

from aws.tools import get_cert_value, create_cert_path, get_schedule
from wc_gc.schemas import LoginConfig
from wc_gc.booking import BookingSystem

logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    try:
        # Block insecure request warnings (temp fix)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        logger.info("Starting tee time booking process...")

        current_time = datetime.now()
        logger.info(f"Current time: {current_time}")

        MEMBER_ID = os.getenv("GOLF_MEMBER_ID")
        MEMBER_PIN = os.getenv("GOLF_PIN")
        BASE_URL = os.getenv("BASE_URL")
        SCHEDULE_ARN = os.getenv("SCHEDULE_ARN")
        logger.info("Retrieved environment variables")

        BOOKING_SCHEDULE = get_schedule(SCHEDULE_ARN)
        logger.info("Retrieved booking schedule")

        config = LoginConfig(
            member_id=MEMBER_ID,
            member_pin=MEMBER_PIN,
            base_url=BASE_URL,
            certificate_path=False,
            schedule=BOOKING_SCHEDULE,
        )

        booking_system = BookingSystem(config)

        if booking_system.login():
            logger.info("Login successful")
            booking_system.load_booking_page()
            target_time = current_time.replace(
                hour=21, minute=0, second=0, microsecond=0
            )

            logger.info(f"Waiting until target time: {target_time}")

            while datetime.now() < target_time:
                time.sleep(0.1)

            execution_time = datetime.now()
            logger.info(f"Attempting to book tee time (time:{execution_time})")

            booking_system.book_tee_time()

            booking_system.close_session()

            logger.info("Tee time booked successfully")
            return {"statusCode": 200, "message": "Tee time booked successfully"}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "message": f"Error: {str(e)}"}),
        }

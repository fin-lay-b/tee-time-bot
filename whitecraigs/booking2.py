from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from whitecraigs.schemas import BookingSchedule, LoginConfig


class TeeTimeBooker:
    def __init__(
        self,
        session: requests.Session,
        config: BookingSchedule,
        certificate_path: str,
        day_delta: int = 3,
    ):
        if not session.url:
            raise ValueError("Session URL is not set. Make a valid request first.")
        self.session = session
        self._base_url = session.url

        self.config = config
        self.certificate_path = certificate_path

        self._booking_date = date.today() + timedelta(day_delta)
        self._booking_date_day = self._booking_date.strftime("%A")
        self._formatted_booking_date = self._booking_date.strftime("%d-%m-%Y")

        self._initial_response = self.nav_to_booking_page()

    @property
    def booking_date(self):
        return self._formatted_booking_date

    @property
    def booking_date_day(self):
        return self._booking_date_day

    @property
    def all_tee_times(self):
        soup = BeautifulSoup(self._initial_response.text, "html.parser")
        time_slots = soup.find_all("th", class_="slot-time")

        tee_times = []
        for slot in time_slots:
            time = slot.text.strip()
            tee_times.append(time)

        return tee_times

    def nav_to_booking_page(self):
        booking_url = f"{self._base_url}?date={self.booking_date}"
        return self.session.get(booking_url, verify=self.certificate_path)

    def select_tee_time(self):
        # Identify tee times in provided range
        # use self.all_tee_times and self.config.booking_schedule (a )

        # loop through the tee times either from earliest or latest and select the first available
        pass

    def book_tee_time(self):
        booking_date_response = self.nav_to_booking_date()
        if not booking_date_response.ok:
            print("❌ Failed to navigate to booking date.")
            return False

        # identify what day it is to figure out what slots are desired

    def _booking_pattern(self) -> list:
        """Checks the tee times available for the day against the desired booking schedule and returns the pattern of booking times that should be followed."""
        # Get all the tee times available for the day
        all_tee_times = self.all_tee_times

        # Get the booking schedule for the day
        start = self.config.schedule[self.booking_date_day]["start"]
        end = self.config.schedule[self.booking_date_day]["end"]
        orient = self.config.schedule[self.booking_date_day]["range_orient"]

        # Select all tee times witin range of start and end
        booking_pattern = []
        for times in all_tee_times:
            if start <= times <= end:
                booking_pattern.append(times)

        if orient == "latest":
            booking_pattern.reverse()

        return booking_pattern

    def _select_rows(html, hour: str, min: str):

        soup = BeautifulSoup(html, "html.parser")

        # Filter ensures only available and desired slots are selected
        class_filter = [
            "future",
            "bookable",
            f"teetime-mins-{min}",
            f"teetime-hours-{hour}",
            "cantreserve",
            "odd",
        ]

        # List of class elements for each row is returned and filtered
        filtered_rows = soup.find_all(
            "tr",
            class_=lambda class_list: class_list
            and all(cls in class_list for cls in class_filter),
        )

        return filtered_rows

    def _get_inputs(row: str):

        # Initialise dictionary to store hidden inputs
        inputs = {}

        # Set numslots to 1 so don't have to input any other player data
        inputs["numslots"] = "1"

        # Initialise BeautifulSoup object
        soup = BeautifulSoup(row, "html.parser")

        # Find all hidden inputs in selected row
        for hidden_inputs in soup.find_all("input", {"type": "hidden"}):
            inputs[hidden_inputs["name"]] = hidden_inputs["value"]

        # Remove inputs that are not required for payload
        keys_to_remove = ["holes"]
        inputs = {k: v for k, v in inputs.items() if k not in keys_to_remove}

        return inputs

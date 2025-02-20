import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup

from .schemas import LoginConfig


class BookingSystem:

    def __init__(self, config: LoginConfig, day_delta: int = 10):
        self.config = config
        self.session = requests.Session()

        self.session.verify = self.config.certificate_path

        self._booking_date = date.today() + timedelta(day_delta)
        self._booking_date_day = self._booking_date.strftime("%A")
        self._formatted_booking_date = self._booking_date.strftime("%d-%m-%Y")

    def login(self):
        login_data = {"memberid": self.config.member_id, "pin": self.config.member_pin}
        login_response = self._make_request(
            "POST", self.config.base_url, data=login_data
        )
        return login_response

    def load_booking_page(self):
        book_response = self._make_request(
            "GET", f"{self.config.base_url}memberbooking/"
        )
        if "code of conduct" not in book_response.text.lower():
            return book_response
        conduct_response = self._make_request(
            "GET",
            f"{self.config.base_url}ttbconsent.php?action=accept",
            allow_redirects=True,
        )
        return conduct_response

    def book_tee_time(self):

        booking_url = (
            f"{self.config.base_url}memberbooking/?date={self._formatted_booking_date}"
        )

        booking_page = self._make_request("GET", booking_url)

        preferred_tee_times = self.config.schedule[self._booking_date_day]

        for time in preferred_tee_times:

            hour, minute = time.split(":")
            row = self._select_row(booking_page.text, hour, minute)

            if row:
                booking_inputs = self._get_inputs(str(row))
                booking_response = self._make_request(
                    "GET", booking_url, params=booking_inputs
                )
                return booking_response

        raise ValueError("No available tee times found")

    def close_session(self):
        self.session.close()

    def _make_request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def _select_row(self, html, hour: str, min: str):

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
        filtered_row = soup.find_all(
            "tr",
            class_=lambda class_list: class_list
            and all(cls in class_list for cls in class_filter),
        )

        return filtered_row

    def _get_inputs(self, row: str):

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

"""A module for automating golf tee time bookings at Whitecraigs Golf Club.

This module provides functionality to login to the golf club booking system,
load booking pages, and make tee time reservations using the intelligentgolf platform.

Functions:
    login(session, url, memberid, pin, cert_path): Authenticates user session with the booking system
    load_booking_page(session, page_url, conduct_url, cert_path): Loads the booking page and accepts conduct terms
    book_tee_time(): Books a tee time (implementation pending)
"""

import requests
from bs4 import BeautifulSoup


# TODO: add in check for wrong credentials (request returns 200 but login fails)
def login(
    session: requests.Session, login_url: str, memberid: str, pin: str, cert_path: str
):
    """Authenticate user session with the provided credentials.

    Args:
        session: The session object to maintain connection state
        login_url: The login endpoint URL
        memberid: User's member identification
        pin: User's PIN number
        cert_path: Path to SSL certificate for verification

    Returns:
        requests.Response: Response object from the login request if successful
        None: If the request fails

    Raises:
        requests.exceptions.RequestException: If the login request fails
    """
    try:
        # Use login data to authenticate session
        login_response = session.post(
            login_url,
            data={"memberid": memberid, "pin": pin},
            verify=cert_path,
        )

        # Check for errors in the login response
        login_response.raise_for_status()

        return login_response

    except requests.exceptions.RequestException as e:
        print(f"[login] Failed: {e}")


def load_booking_page(
    session: requests.Session, booking_page_url: str, conduct_url: str, cert_path: str
):
    """Load the booking page and accept conduct terms.

    Args:
        session: Active session object with authentication
        booking_page_url: URL of the booking page
        conduct_url: URL to accept conduct terms
        cert_path: Path to SSL certificate for verification

    Returns:
        requests.Response: Response object from the conduct terms acceptance
        None: If either request fails

    Raises:
        requests.exceptions.RequestException: If any request fails
    """
    try:
        # Load the booking page
        booking_page_response = session.get(booking_page_url, verify=cert_path)
        # Check for errors in the booking page response
        booking_page_response.raise_for_status()

        # Accept conduct terms to proceed to booking page
        conduct_response = session.get(
            conduct_url, allow_redirects=True, verify=cert_path
        )
        # Check for errors in the conduct response
        conduct_response.raise_for_status()

        return conduct_response

    except requests.exceptions.RequestException as e:
        print(f"[load_booking_page] Failed: {e}")


def book_tee_time(
    session: requests.Session,
    booking_date_url: str,
    booking_date: str,
    booking_time: str,
    token_key: str,
    token_value: str,
    cert_path: str,
):
    """Book a tee time with the specified parameters.

    Args:
        session: Active session object with authentication
        booking_date_url: URL of the booking page
        booking_date: Date for the tee time in DD-MM-YYYY format
        booking_time: Time for the tee time in HH:MM:SS format
        token_key: Security token key required for booking
        token_value: Security token value required for booking
        cert_path: Path to SSL certificate for verification

    Returns:
        requests.Response: Response object from the booking request if successful
        None: If the request fails

    Raises:
        requests.exceptions.RequestException: If the booking request fails
    """
    try:
        # Make the booking request with required parameters
        booking_response = session.get(
            booking_date_url,
            params={
                "numslots": "1",
                "date": booking_date,
                "course": "1081",
                "group": "1",
                "book": booking_time,
                token_key: token_value,
            },
            verify=cert_path,
        )
        # Check for errors in the booking response
        booking_response.raise_for_status()

        return booking_response

    except requests.exceptions.RequestException as e:
        print(f"[book_tee_time] Failed: {e}")


def select_table_row(
    session: requests.Session,
    booking_date_url: str,
    booking_date: str,
    booking_time: str,
    cert_path: str,
):
    """
    Selects a table row from the booking page for a specific time and date

    Args:
        session (requests.Session): Active session with golf booking website
        booking_date_url (str): URL of the booking page for specific date
        booking_date (str): Date to book in format "YYYY-MM-DD"
        booking_time (str): Time to book in format "HH:MM"
        cert_path (str): Path to SSL certificate file

    Returns:
        BeautifulSoup.Tag: Table row element containing the selected tee time or None if not found

    Raises:
        requests.exceptions.RequestException: If there's an error getting the booking page
    """

    try:
        # Split booking_time into hour and minute
        hour, minute = booking_time.split(":")

        # Get the booking page HTML
        html = session.get(booking_date_url, verify=cert_path).text
        soup = BeautifulSoup(html, "lxml")

        # Filter ensures only available and desired slots are selected
        class_filter = [
            f"teetime-mins-{minute}",
            f"teetime-hours-{hour}",
        ]

        # Helper function to apply class filter to all "tr" (row) elements
        def has_all_classes(row_classes):
            # Prevent error with short-circuit then filter
            return row_classes and all(cls in row_classes for cls in class_filter)

        # Find the first "tr" element with all classes in class_filter (.find() behaves the same as .find_all() but returns the first match)
        row = soup.find(
            "tr",
            class_=has_all_classes,
        )

        return row

    except requests.exceptions.RequestException as e:
        print(f"[get_booking_tokens] Failed: {e}")


def get_inputs(row: str):

    try:

        # Initialise dictionary to store hidden inputs
        inputs = {}

        # Set numslots to 1 so don't have to input any other player data
        inputs["numslots"] = "1"

        # Initialise BeautifulSoup object
        soup = BeautifulSoup(row, "lxml")

        # Find all hidden inputs in selected row
        for hidden_inputs in soup.find_all("input", {"type": "hidden"}):
            inputs[hidden_inputs["name"]] = hidden_inputs["value"]

        # del inputs["holes"]

        return inputs

    except Exception as e:
        print(f"[get_booking_tokens] Failed: {e}")


if __name__ == "__main__":
    s = requests.Session()

    CERT_PATH = "./zscaler-root-ca.crt"

    login_response = login(
        s,
        "https://whitecraigs.intelligentgolf.co.uk/",
        memberid="7109",
        pin="1866",
        cert_path=CERT_PATH,
    )

    load_response = load_booking_page(
        s,
        "https://whitecraigs.intelligentgolf.co.uk/memberbooking/",
        "https://whitecraigs.intelligentgolf.co.uk/ttbconsent.php?action=accept",
        cert_path=CERT_PATH,
    )
    print(load_response.status_code)

    row = select_table_row(
        s,
        "https://whitecraigs.intelligentgolf.co.uk/memberbooking/?date=29-04-2025",
        booking_date="29-04-2025",
        booking_time="20:00",
        cert_path=CERT_PATH,
    )

    print(row)

    inputs = get_inputs(str(row))
    print(inputs)

    # s.post(
    #     "https://whitecraigs.intelligentgolf.co.uk/",
    #     data={"memberid": "7109", "pin": "1866"},
    #     verify=False,
    # )

    # response1 = s.get(
    #     "https://whitecraigs.intelligentgolf.co.uk/memberbooking/",
    #     verify=False,
    # )
    # print(response1.text)

    # response2 = s.get(
    #     "https://whitecraigs.intelligentgolf.co.uk/ttbconsent.php?action=accept",
    #     allow_redirects=True,
    #     verify=False,
    # )

    # response3 = s.post(
    #     "https://whitecraigs.intelligentgolf.co.uk/memberbooking/",
    #     verify=False,
    #     data={"date": "24-04-2025"},
    # )

    # print(response3.text)

    # response4 = s.get(
    #     "https://whitecraigs.intelligentgolf.co.uk/memberbooking/",
    #     params={
    #         "numslots": "1",
    #         "date": "16-04-2025",
    #         "course": "1081",
    #         "group": "1",
    #         "book": "17:15:00",
    #         "3814d9825796571fa31b6b4414471be24f492d8f790cd9330ff4d55f7c42590a": "1355084a2141983311cded666a325d69f6d100246a0f460e2fc363250442bd0b",
    #     },
    #     verify=False,
    # )

{
    "numslots": "1",
    "date": "29-04-2025",
    "course": "1081",
    "group": "1",
    "book": "20:00:00",
    "a18d4095ff45451808e69a7645000d50e7124976f83f736cfae569809b66ed9d": "33dd60fa42aef307e4cd41665e3ca808697d737c66072ce0a692b426614b60d0",
}

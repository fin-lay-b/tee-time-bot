import requests


def login(session: requests.Session, url: str, memberid: str, pin: str):
    response = session.post(
        url,
        data={"memberid": memberid, "pin": pin},
    )
    return response


def load_booking_page(
    session: requests.Session,
    page_url: str,
):
    # Navigate to the booking page and accept the code of conduct
    pass


def book_tee_time():
    pass


if __name__ == "__main__":
    s = requests.Session()

    s.post(
        "https://whitecraigs.intelligentgolf.co.uk/",
        data={"memberid": "7109", "pin": "1866"},
        verify=False,
    )

    response1 = s.get(
        "https://whitecraigs.intelligentgolf.co.uk/memberbooking/",
        verify=False,
    )
    print(response1.text)

    response2 = s.get(
        "https://whitecraigs.intelligentgolf.co.uk/ttbconsent.php?action=accept",
        allow_redirects=True,
        verify=False,
    )

    response3 = s.post(
        "https://whitecraigs.intelligentgolf.co.uk/memberbooking/",
        verify=False,
        data={"date": "24-04-2025"},
    )

    print(response3.text)

    response4 = s.get(
        "https://whitecraigs.intelligentgolf.co.uk/memberbooking/",
        params={
            "numslots": "1",
            "date": "16-04-2025",
            "course": "1081",
            "group": "1",
            "book": "17:15:00",
            "3814d9825796571fa31b6b4414471be24f492d8f790cd9330ff4d55f7c42590a": "1355084a2141983311cded666a325d69f6d100246a0f460e2fc363250442bd0b",
        },
        verify=False,
    )

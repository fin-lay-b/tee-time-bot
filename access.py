# # ADD TO README
# # requests does not trust Zsclaer certificates by default. To solve:
# # 1. Open https://whitecraigs.intelligentgolf.co.uk in a browser.
# # 2. Go to the padlock or setting icon in the address bar.
# # 3. Select "Certificate is valid".
# # 4. From the top root of details tap, export the certificate to a file and save it in the same directory as this script.
# # 5. Make sure the file path is included in the .gitignore file.


import os
import requests
from dotenv import load_dotenv
from claude import book_tee_time
from bs4 import BeautifulSoup


LOGIN_URL = "https://whitecraigs.intelligentgolf.co.uk/"
CERTIFICATE_PATH = "./Zscaler Root CA.crt"
BOOKING_URL = "https://whitecraigs.intelligentgolf.co.uk/memberbooking/"
CONDUCT_FORM_URL = (
    "https://whitecraigs.intelligentgolf.co.uk/ttbconsent.php?action=accept"
)

# Load environment variables
load_dotenv()
member_id = os.getenv("GOLF_MEMBER_ID")
pin = os.getenv("GOLF_PIN")


session = requests.Session()

# Step 1: Login
login_data = {"memberid": member_id, "pin": pin}
response = session.post(LOGIN_URL, data=login_data, verify=CERTIFICATE_PATH)

if response.ok:
    print("✅ Login successful")

    # Step 2: Check if Code of Conduct is required
    booking_response = session.get(BOOKING_URL, verify=CERTIFICATE_PATH)

    if booking_response.ok:
        if "code of conduct" in booking_response.text.lower():
            print("⚠️ Code of Conduct page detected! Accepting...")

            # Step 3: Accept Code of Conduct via GET request
            conduct_response = session.get(
                CONDUCT_FORM_URL, verify=CERTIFICATE_PATH, allow_redirects=True
            )

            if conduct_response.ok:
                print("✅ Code of Conduct accepted!")

                # Step 4: Re-attempt loading the booking page
                final_booking_response = session.get(
                    BOOKING_URL, verify=CERTIFICATE_PATH
                )
                if final_booking_response.ok:
                    print(
                        "✅ Booking page loaded successfully after accepting Conduct!"
                    )

                    soup = BeautifulSoup(final_booking_response.text, "html.parser")
                    hidden_inputs = soup.find_all("input", type="hidden")
                    payload = {
                        "numslots": "1",  # Change as needed
                        "date": "05-02-2025",  # Change as needed
                        "course": "1081",
                        "group": "1",
                        "book": "19:00:00",  # Change as needed
                    }

                    # Add hidden security token dynamically
                    desired_time = (
                        "19:00:00"  # Example: Change this to the actual tee time
                    )

                    # Find the section containing the correct tee time
                    tee_time_section = None
                    for section in soup.find_all(
                        "div", class_="teetime-container"
                    ):  # Update class as needed
                        if desired_time in section.get_text():
                            tee_time_section = section
                            break  # Stop once the correct section is found

                    if not tee_time_section:
                        print("Tee time not found!")
                    else:
                        # Extract hidden inputs from the correct section
                        hidden_inputs = tee_time_section.find_all(
                            "input", type="hidden"
                        )

                        # Build the correct payload
                        payload = {
                            hidden["name"]: hidden["value"] for hidden in hidden_inputs
                        }

                        print("Correct Payload:", payload)

                    # booking_data = {
                    #     "numslots": "1",
                    #     "date": "05-02-2025",
                    #     "course": "1081",
                    #     "group": "1",
                    #     "book": "19:00:00",
                    #     "2b1b85455190d734d11a31f33f75d1487b456ba0951b062f69357b99eeeca232": "347080fd6c0947888cceb6d0a2d924953c0299b08df2f529cd1ab0a1b4c33532",
                    # }

                    book_time = session.get(
                        BOOKING_URL, params=payload, verify=CERTIFICATE_PATH
                    )

                    if book_time.ok:
                        print("✅ Booking successful!")
                        # print(book_time.text)
                    else:
                        print("❌ Failed to book tee time.")
                        # print(book_time.text)

                else:
                    print("❌ Failed to load booking page after accepting Conduct.")
            else:
                print("❌ Failed to accept Code of Conduct.")
        else:
            print("✅ No Code of Conduct page detected, booking page is accessible.")
    else:
        print("❌ Booking page failed to load.")
else:
    print("❌ Login failed")

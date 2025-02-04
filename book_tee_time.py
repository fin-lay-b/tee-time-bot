# import os

# import requests
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv

# # ADD TO README
# # requests does not trust Zsclaer certificates by default. To solve:
# # 1. Open https://whitecraigs.intelligentgolf.co.uk in a browser.
# # 2. Go to the padlock or setting icon in the address bar.
# # 3. Select "Certificate is valid".
# # 4. From the top root of details tap, export the certificate to a file and save it in the same directory as this script.
# # 5. Make sure the file path is included in the .gitignore file.

# # Store the member ID and PIN as environment variables (or some other secure method).
# CERTIFICATE_PATH = "./Zscaler Root CA.crt"

# load_dotenv()
# member_id = os.getenv("GOLF_MEMBER_ID")
# pin = os.getenv("GOLF_PIN")

# login_url = "https://whitecraigs.intelligentgolf.co.uk/"

# login_data = {"memberid": member_id, "pin": pin}

# session = requests.Session()

# response = session.post(login_url, data=login_data, verify=CERTIFICATE_PATH)

# # if response.ok:
# #     print("Login successful")
# #     booking_url = "https://whitecraigs.intelligentgolf.co.uk/memberbooking/"
# #     booking_response = session.get(booking_url, verify=CERTIFICATE_PATH)

# #     if booking_response.ok:
# #         print("Booking page loaded")
# #         # print(booking_response.text)
# #         conduct_data = {"action": "accept"}
# #         conduct_response = session.post(
# #             booking_url, data=conduct_data, verify=CERTIFICATE_PATH
# #         )

# #         if conduct_response.ok:
# #             print("Conduct page loaded")
# #             print(conduct_response.text)

# #         else:
# #             print("Conduct page failed to load")
# #     else:
# #         print("Booking page failed to load")


# # else:
# #     print("Login failed")


import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CERTIFICATE_PATH = "./Zscaler Root CA.crt"

# Member credentials
member_id = os.getenv("GOLF_MEMBER_ID")
pin = os.getenv("GOLF_PIN")

login_url = "https://whitecraigs.intelligentgolf.co.uk/"
booking_url = "https://whitecraigs.intelligentgolf.co.uk/memberbooking/"
conduct_url = "https://whitecraigs.intelligentgolf.co.uk/ttbconsent.php?action=accept"

session = requests.Session()

# Step 1: Login
login_data = {"memberid": member_id, "pin": pin}
response = session.post(login_url, data=login_data, verify=CERTIFICATE_PATH)

if response.ok:
    print("✅ Login successful")

    # Step 2: Check if Code of Conduct is required
    booking_response = session.get(booking_url, verify=CERTIFICATE_PATH)

    if booking_response.ok:
        if "code of conduct" in booking_response.text.lower():
            print("⚠️ Code of Conduct page detected! Accepting...")

            # Step 3: Accept Code of Conduct via GET request
            conduct_response = session.get(
                conduct_url, verify=CERTIFICATE_PATH, allow_redirects=True
            )

            if conduct_response.ok:
                print("✅ Code of Conduct accepted!")

                # Step 4: Re-attempt loading the booking page
                final_booking_response = session.get(
                    booking_url, verify=CERTIFICATE_PATH
                )
                if final_booking_response.ok:
                    print(
                        "✅ Booking page loaded successfully after accepting Conduct!"
                    )
                    print(final_booking_response.text)
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

import os
import requests

# ADD TO README
# requests does not trust Zsclaer certificates by default. To solve:
# 1. Open https://whitecraigs.intelligentgolf.co.uk in a browser.
# 2. Go to the padlock or setting icon in the address bar.
# 3. Select "Certificate is valid".
# 4. From the top root of details tap, export the certificate to a file and save it in the same directory as this script.
# 5. Make sure the file path is included in the .gitignore file.

# Store the member ID and PIN as environment variables (or some other secure method).
member_id = os.getenv("MEMBER_ID")
pin = os.getenv("PIN")

login_url = "https://whitecraigs.intelligentgolf.co.uk/"

login_data = {"memberid": member_id, "pin": pin}

session = requests.Session()

response = session.post(login_url, data=login_data, verify="./Zscaler Root CA.crt")

if response.ok:
    print("Login successful")

else:
    print("Login failed")

from bs4 import BeautifulSoup


def select_rows(html, hour: str, min: str):

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


def get_inputs(row: str):

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


if __name__ == "__main__":

    def all_tee_times(html):
        soup = BeautifulSoup(html, "html.parser")
        time_slots = soup.find_all("th", class_="slot-time")

        tee_times = []
        for slot in time_slots:
            time = slot.text.strip()
            tee_times.append(time)

        return tee_times

    with open("./booking_response.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # rows = select_rows(str(html_content), "21", "00")

    # if rows:  # Check if any rows were found
    #     # Convert the first row to string and pass it
    #     inputs = get_inputs(str(rows))
    #     print(inputs)
    # else:
    #     print("No matching rows found")

    tee_times = all_tee_times(html_content)
    print(tee_times)

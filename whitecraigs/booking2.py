from datetime import date, timedelta, time
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from typing import Optional, Literal
import requests
from bs4 import BeautifulSoup

# booking_schedule = {
#     "Monday": [
#         {"start": "06:00", "end": "06:45", "range_orient": "earliest"},
#         {"start": "18:00", "end": "19:00", "range_orient": "earliest"}
#     ],
#     "Tuesday": [
#         {"start": "16:00", "end": "17:30", "range_orient": "latest"},
#     ],
#     ...

class Booking(BaseModel):
    start: str = Field(pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$", 
                       description="Start time of tee time range in 24-hour format (HH:MM)"
    )
    end: str = Field(pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$",
                     description="End time of tee time range in 24-hour format (HH:MM)"
    )
    range_orient: Literal["earliest", "latest"] = Field(default='earliest', 
                                                        description="Preferred direction to search within range."
    )

    @field_validator('end')
    def end_after_start(cls, v: str, info: ValidationInfo):
        pass

    # @validator('start', 'end', pre=True)
    # def parse_time(cls, v):
    #     if isinstance(v, str):
    #         try:
    #             return time.fromisoformat(v)
    #         except ValueError:
    #             raise ValueError('Time must be in HH:MM format')
    #     return v

    # @validator('end')
    # def end_must_be_after_start(cls, v, values):
    #     if 'start' in values and v <= values['start']:
    #         raise ValueError('End time must be after start time')
    #     return v


class BookingSchedule(BaseModel):
    pass
#     schedule: Dict[str, List[Booking]] = Field(
#         ...,
#         description="Booking schedule with days of the week as keys"
#     )

#     @validator('schedule')
#     def validate_days(cls, v):
#         valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
#         for day in v.keys():
#             if day not in valid_days:
#                 raise ValueError(f'Invalid day: {day}. Must be one of {valid_days}')
#         return v


# Can add more validation restraint to the fields
class TeeTimeConfig(BaseModel):
    session: requests.Session = Field(description="Session object for booking a tee time")
    booking_schedule : BookingSchedule = Field(description="Booking schedule with days of the week as keys")


# booking_schedule = {
#     "Monday": [
#         {"start": "06:00", "end": "06:45", "range_orient": "earliest"},
#         {"start": "18:00", "end": "19:00", "range_orient": "earliest"}
#     ],
#     "Tuesday": [
#         {"start": "16:00", "end": "17:30", "range_orient": "latest"},
#     ],
#     ...

class TeeTimeBooker:
    def __init__(self, config: TeeTimeConfig, day_delta: int = 11):
        self.config = config
        self.todays_date = date.today()
        self.day_delta = day_delta
        self.booking_date = self.todays_date + timedelta(day_delta)
    
    @property
    def booking_date_day(self):
        return self.booking_date.strftime("%A")

    @property
    def formatted_booking_date(self):
        return self.booking_date.strftime("%d-%m-%Y")
    
    @property
    def all_tee_times(self):
        soup = BeautifulSoup(self.config.session.text, "html.parser")
        time_slots = soup.find_all('th', class_='slot-time')

        tee_times = []
        for slot in time_slots:
            time = slot.text.strip()
            tee_times.append(time)
        
        return tee_times
            

    def nav_to_booking_date(self):
        booking_url = f"{self.config.session.url}?date={self.formatted_booking_date}"
        return self.config.session.get(booking_url)

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
        

    def _select_rows(html, hour: str, min: str)

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




from datetime import time
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from typing import Literal, Dict, List
import requests


# Can add more validation restraint to the fields
class LoginConfig(BaseModel):
    member_id: str = Field(..., description="Member ID for golf club")
    member_pin: str = Field(..., description="PIN for golf club")
    login_url: str = Field(..., description="URL for login page")
    certificate_path: str = Field(..., description="Path to certificate")
    booking_url: str = Field(..., description="URL for booking page")
    conduct_form_url: str = Field(..., description="URL for code of conduct form")


class Booking(BaseModel):
    start: str = Field(
        pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$",
        description="Start time of tee time range in 24-hour format (HH:MM)",
    )
    end: str = Field(
        pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$",
        description="End time of tee time range in 24-hour format (HH:MM)",
    )
    range_orient: Literal["earliest", "latest"] = Field(
        default="earliest", description="Preferred direction to search within range"
    )

    @field_validator("end")
    def end_after_start(cls, v: str, info: ValidationInfo):
        if "start" in info.data:
            start_time = time.fromisoformat(info.data["start"])
            end_time = time.fromisoformat(v)
            if end_time <= start_time:
                raise ValueError("End time must be after start time")
        return v


class BookingSchedule(BaseModel):
    pass
    schedule: Dict[str, List[Booking]] = Field(
        ..., description="Booking schedule with days of the week as keys"
    )

    @field_validator("schedule")
    def validate_days(cls, v):
        valid_days = {
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        }
        for day in v.keys():
            if day not in valid_days:
                raise ValueError(f"Invalid day: {day}. Must be one of {valid_days}")
        return v


# class TeeTimeConfig(BaseModel):
#     booking_schedule: BookingSchedule = Field(
#         description="Booking schedule with days of the week as keys"
#     )


if __name__ == "__main__":
    booking_schedule = {
        "schedule": {
            "Monday": [
                {"start": "06:00", "end": "06:45", "range_orient": "earliest"},
                {"start": "18:00", "end": "19:00", "range_orient": "earliest"},
            ],
            "Tuesday": [
                {"start": "16:00", "end": "17:30", "range_orient": "earliest"},
            ],
            "Wednesday": [
                {"start": "16:00", "end": "17:30", "range_orient": "earliest"},
            ],
            "Thursday": [
                {"start": "16:00", "end": "17:30", "range_orient": "earliest"},
            ],
            "Friday": [
                {"start": "16:00", "end": "17:30", "range_orient": "earliest"},
            ],
            "Saturday": [
                {"start": "07:00", "end": "08:30", "range_orient": "latest"},
            ],
            "Sunday": [
                {"start": "07:00", "end": "08:30", "range_orient": "earliest"},
            ],
        }
    }

    validated_schedule = BookingSchedule(**booking_schedule)

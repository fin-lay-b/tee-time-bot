from pydantic import BaseModel, Field
from typing import List


class Schedule(BaseModel):
    Monday: List[str] = Field(default_factory=list)
    Tuesday: List[str] = Field(default_factory=list)
    Wednesday: List[str] = Field(default_factory=list)
    Thursday: List[str] = Field(default_factory=list)
    Friday: List[str] = Field(default_factory=list)
    Saturday: List[str] = Field(default_factory=list)
    Sunday: List[str] = Field(default_factory=list)


class LoginConfig(BaseModel):
    member_id: str = Field(..., description="Member ID for golf club")
    member_pin: str = Field(..., description="PIN for golf club")
    base_url: str = Field(..., description="Base URL for golf club")
    certificate_path: str = Field(..., description="Path to certificate")
    schedule: Schedule = Field(
        ..., description="Booking schedule with days of the week"
    )

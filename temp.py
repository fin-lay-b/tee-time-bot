# class Booking(BaseModel):
#     start: str = Field(..., pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$", description="Start time in 24-hour format (HH:MM)")
#     end: str = Field(..., pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$", description="End time in 24-hour format (HH:MM)")
#     player: str = Field(..., min_length=1)

#     @validator('end')
#     def end_must_be_after_start(cls, v, values):
#         if 'start' in values:
#             start_time = time.fromisoformat(values['start'])
#             end_time = time.fromisoformat(v)
#             if end_time <= start_time:
#                 raise ValueError('End time must be after start time')
#         return v

# class BookingSchedule(BaseModel):
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

if __name__ == "__main__":
    from datetime import date, timedelta

    today = date.today()
    print(today)

    print(today + timedelta(days=11))

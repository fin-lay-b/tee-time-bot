import requests
from typing import Optional
from pydantic import BaseModel


class BookingConfig(BaseModel):
    member_id: str
    member_pin: str
    login_url: str
    certificate_path: str
    booking_url: str
    conduct_form_url: str


class BookingSession:
    def __init__(self, config: BookingConfig):
        self.member_id: str = config.member_id
        self.member_pin: str = config.member_pin
        self.login_url: str = config.login_url
        self.certificate_path: str = config.certificate_path
        self.booking_url: str = config.booking_url
        self.conduct_form_url: str = config.conduct_form_url
        self._session: Optional[requests.Session] = None

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

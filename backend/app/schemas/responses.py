from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List
import datetime


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


# ----------------- Users -----------------
class UserResponse(BaseResponse):
    status: str
    token: str


class UserMeResponse(BaseResponse):
    email: EmailStr
    phone: str
    name: str
    role: str

class UserAdminResponse(BaseResponse):
    id: str
    email: EmailStr
    phone: str
    name: str
    role: str


class UserListResponse(BaseResponse):
    users: List[UserAdminResponse]


class UserRolerResponse(BaseResponse):
    role: str


# ----------------- Events -----------------
class EventSchema(BaseResponse):
    id: str
    name: str
    type: str
    desc: str
    date: datetime.datetime
    duration: datetime.timedelta
    venue: str


class EventListResponse(BaseResponse):
    events: List[EventSchema]


class RegistrationResponse(BaseResponse):
    name: str
    email: EmailStr

class WinnerResponse(BaseResponse):
    name: str
    position: int
    prize: str

# ----------------- Schedule -----------------
class ScheduleResponse(BaseResponse):
    name: str
    start_time: str
    venue: str

# ----------------- Student -----------------
class StudentResponse(BaseResponse):
    roll: str
    dept: str


class StudentVolunteerResponse(BaseResponse):
    name: str
    roll: str
    dept: str


# ----------------- Participant -----------------
class ParticipantResponse(BaseResponse):
    name: str
    email: EmailStr
    phone: str
    university: str
    accomodation: str
    mess: str

class MiniParticipantResponse(BaseResponse):
    name: str
    email: EmailStr
    university: str
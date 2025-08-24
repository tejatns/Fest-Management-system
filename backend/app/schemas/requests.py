from pydantic import BaseModel, EmailStr, Field, validator
import datetime
from typing import List, Optional


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


# ----------------- Users -----------------
class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    phone: Optional[str] = None
    name: str
    role: str

class UserChangeRequest(BaseRequest):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None


class UserLoginRequest(BaseRequest):
    email: EmailStr
    password: str


class BaseUser(BaseModel):
    id: str
    email: EmailStr
    phone: str
    role: str
    password: str
    name: str


# ----------------- Students -----------------
class StudentCreateRequest(BaseRequest):
    roll: str
    dept: str


class StudentVolunteerRequest(BaseRequest):
    event_id: str


# ----------------- Events -----------------
class EventCreateRequest(BaseRequest):
    name: str
    type: str
    desc: str
    date: datetime.datetime
    duration: datetime.timedelta
    venue: str


class EventChangeRequest(BaseRequest):
    name: Optional[str] = None
    type: Optional[str] = None
    desc: Optional[str] = None
    date: Optional[datetime.datetime] = None
    duration: Optional[datetime.timedelta] = None
    venue: Optional[str] = None


# ----------------- Schedule -----------------
class ScheduleRequest(BaseRequest):
    date: str

# ----------------- Student -----------------
# ----------------- Participant -----------------
class ParticipantCreateRequest(BaseRequest):
    university: str

"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""

import uuid

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Annotated
import datetime

MINI_STRING = 30
MEDIUM_STRING = 120
LONG_STRING = 300


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)
    phone: Mapped[str] = mapped_column(
        String(MINI_STRING), nullable=True, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        String(MEDIUM_STRING), nullable=False, unique=True, index=True
    )
    role: Mapped[str] = mapped_column(String(MINI_STRING), nullable=False)
    password: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)


class Student(Base):
    __tablename__ = "student"
    id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    roll: Mapped[str] = mapped_column(
        String(MINI_STRING), nullable=False, unique=True, index=True
    )
    dept: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)


class Accomodation(Base):
    __tablename__ = "accomodation"
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(MINI_STRING), nullable=False, unique=True, index=True
    )
    location: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)


class Mess(Base):
    __tablename__ = "mess"
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(MINI_STRING), nullable=False, unique=True, index=True
    )
    location: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)


class Participant(Base):
    __tablename__ = "participant"
    id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    university: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)
    accomodation_id: Mapped[str] = mapped_column(
        ForeignKey("accomodation.id", ondelete="SET NULL", onupdate="SET NULL"),
        nullable=True,
    )
    mess_id: Mapped[str] = mapped_column(
        ForeignKey("mess.id", ondelete="SET NULL", onupdate="SET NULL"), nullable=True
    )


class Venue(Base):
    __tablename__ = "venue"
    name: Mapped[str] = mapped_column(
        String(MINI_STRING), primary_key=True, unique=True, nullable=False
    )
    location: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)


class Event(Base):
    __tablename__ = "event"
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(MINI_STRING), nullable=False, unique=True, index=True
    )
    type: Mapped[str] = mapped_column(String(MINI_STRING), nullable=False)
    desc: Mapped[str] = mapped_column(String(LONG_STRING))
    date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    duration: Mapped[datetime.timedelta] = mapped_column(nullable=False)
    venue: Mapped[str] = mapped_column(
        ForeignKey("venue.name", ondelete="SET NULL", onupdate="SET NULL"),
        nullable=True,
    )


class Registration(Base):
    __tablename__ = "registration"
    event_id: Mapped[str] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    reg_time: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now
    )


class Volunteer(Base):
    __tablename__ = "volunteer"
    id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    event_id: Mapped[str] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )


class Manage(Base):
    __tablename__ = "manage"
    id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    position: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)
    responsibility: Mapped[str] = mapped_column(String(LONG_STRING), nullable=False)
    event_id: Mapped[str] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )


class Competition(Base):
    __tablename__ = "competition"
    id: Mapped[str] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    props: Mapped[str] = mapped_column(String(MEDIUM_STRING), nullable=False)


class Prize(Base):
    __tablename__ = "prize"
    event_id: Mapped[str] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    position: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    winner_id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL", onupdate="SET NULL"),
        nullable=True,
    )


class Sponsor(Base):
    __tablename__ = "sponsor"
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(MINI_STRING), nullable=False, unique=True, index=True
    )
    desc: Mapped[str] = mapped_column(String(LONG_STRING))


class Sponsorship(Base):
    __tablename__ = "sponsorship"
    sponsor_id: Mapped[str] = mapped_column(
        ForeignKey("sponsor.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    event_id: Mapped[str] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

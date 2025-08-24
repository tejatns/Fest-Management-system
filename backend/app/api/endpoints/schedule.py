import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Event
from app.schemas.responses import List, ScheduleResponse
from app.schemas.requests import BaseUser, ScheduleRequest


router = APIRouter()


def unique_list(l):
    return list(dict.fromkeys(l))


@router.get("/dates", response_model=List[str], status_code=status.HTTP_200_OK)
async def read_schedule_dates(
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Get schedule dates"""
    dates = await session.execute(select(Event.date).order_by(Event.date))
    dates = dates.scalars().all()
    return unique_list(
        [
            date.strftime("%d-%m-%Y")
            for date in sorted(dates, key=lambda x: int(x.strftime("%d%m%Y")))
        ]
    )


@router.get(
    "/{date}", response_model=List[ScheduleResponse], status_code=status.HTTP_200_OK
)
async def read_schedule(
    date: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Get schedule for a date"""
    event_date = datetime.datetime.strptime(date, "%d-%m-%Y")
    events = await session.execute(select(Event))
    events = events.scalars().all()
    schedule = []
    for event in events:
        if event.date.date() != event_date.date():
            continue
        schedule.append(
            ScheduleResponse(
                name=event.name,
                start_time=event.date.strftime("%H:%M"),
                venue=event.venue,
            )
        )

    return schedule

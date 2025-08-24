from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DBAPIError

from app.api import deps
from app.models import Event, Manage, Participant, Prize, User, Registration
from app.schemas.responses import (
    EventListResponse,
    List,
    EventSchema,
    RegistrationResponse,
    WinnerResponse,
)
from app.schemas.requests import EventChangeRequest, BaseUser


router = APIRouter()


@router.get("/all", response_model=EventListResponse, status_code=status.HTTP_200_OK)
async def list_events(
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """List all events"""
    result = await session.execute(select(Event))
    events = result.scalars().all()

    all_events: List[EventSchema] = []
    for event in events:
        all_events.append(
            EventSchema(
                id=event.id,
                name=event.name,
                type=event.type,
                desc=event.desc,
                date=event.date,
                duration=event.duration,
                venue=event.venue,
            )
        )
    return EventListResponse(events=all_events)


@router.put("/register/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_students(
    event_id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Register for an event"""
    if current_user.role != "participant" and current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not a participant"
        )

    event = await session.execute(select(Event).filter(Event.id == event_id))
    event = event.scalar_one()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    try:
        registration = Registration(event_id=event_id, user_id=current_user.id)
        session.add(registration)
        await session.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already registered as Participant",
        )
    except DBAPIError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Already registered as Volunteer",
        )


def formatINR(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "₹ " + "".join([r] + d)


@router.get(
    "/winners/{event_id}",
    response_model=List[WinnerResponse],
    status_code=status.HTTP_200_OK,
)
async def list_winners(
    event_id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """List all winners for an event"""
    try:
        result = await session.execute(select(Prize).filter(Prize.event_id == event_id))
        prizes = result.scalars().all()
        if len(prizes) == 0:
            return []
    except Exception as e:
        print(e)
        return []

    all_winners: List[WinnerResponse] = []
    for prize in prizes:
        if prize.winner_id is not None:
            user = await session.execute(
                select(User).filter(User.id == prize.winner_id)
            )
            user = user.scalar_one()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inconsistent data",
                )
        all_winners.append(
            WinnerResponse(
                name=user.name if prize.winner_id is not None else "Not declared",
                position=prize.position,
                prize=formatINR(prize.amount),
            )
        )

    all_winners.sort(key=lambda x: x.position)
    return all_winners


# ----------------------------- Restricted -----------------------------
@router.post("/", response_model=EventSchema, status_code=201)
async def create_event(
    event: EventSchema,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Create an event"""
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_event = Event(
        id=event.id,
        name=event.name,
        type=event.type,
        desc=event.desc,
        date=event.date,
        time=event.time,
        venue=event.venue,
    )
    session.add(new_event)
    await session.commit()
    return new_event


@router.put("/{id}", response_model=EventSchema, status_code=status.HTTP_200_OK)
async def update_event(
    id: str,
    new_event: EventChangeRequest,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Update an event"""
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await session.execute(select(Event).where(Event.id == id))
    event = result.scalars().first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event.name = new_event.name if new_event.name else event.name
    event.type = new_event.type if new_event.type else event.type
    event.desc = new_event.desc if new_event.desc else event.desc
    event.date = new_event.date if new_event.date else event.date
    event.time = new_event.time if new_event.time else event.time
    event.venue = new_event.venue if new_event.venue else event.venue
    await session.commit()
    return EventSchema(
        id=event.id,
        name=event.name,
        type=event.type,
        desc=event.desc,
        date=event.date,
        time=event.time,
        venue=event.venue,
    )


@router.get(
    "/registrations/{event_id}",
    response_model=List[RegistrationResponse],
    status_code=status.HTTP_200_OK,
)
async def list_registrations(
    event_id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """List all registrations for an event"""
    organizers = await session.execute(
        select(Manage).filter(Manage.event_id == event_id)
    )
    organizers = organizers.scalars().all()
    if current_user.role == "admin" or (
        current_user.role == "organizer"
        and current_user.id in [organizer.id for organizer in organizers]
    ):
        result = await session.execute(
            select(Registration).filter(Registration.event_id == event_id)
        )
        registrations = result.scalars().all()
        all_registrations: List[RegistrationResponse] = []
        for registration in registrations:
            user = await session.execute(
                select(User).filter(User.id == registration.user_id)
            )
            user = user.scalar_one()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inconsistent data",
                )
            all_registrations.append(
                RegistrationResponse(name=user.name, email=user.email)
            )

        return all_registrations
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

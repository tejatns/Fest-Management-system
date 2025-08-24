from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Accomodation, Manage, Mess, Participant
from app.schemas.responses import MiniParticipantResponse, ParticipantResponse
from app.schemas.requests import BaseUser, ParticipantCreateRequest


router = APIRouter()


@router.post(
    "/me", response_model=ParticipantResponse, status_code=status.HTTP_201_CREATED
)
async def create_participant(
    new_participant: ParticipantCreateRequest,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Create a new participant"""
    participant = Participant(
        id=current_user.id,
        university=new_participant.university,
    )
    session.add(participant)
    await session.commit()

    participant_in_db = await session.execute(
        select(Participant).filter(Participant.id == current_user.id)
    )
    participant_in_db = participant_in_db.scalar_one()
    if participant_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Inconsistent data",
        )
    accomodation, mess = None, None
    if participant_in_db.accomodation_id:
        accomodation = await session.execute(
            select(Accomodation).filter(
                Accomodation.id == participant_in_db.accomodation_id
            )
        )
        accomodation = accomodation.scalar_one()
        if accomodation is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Inconsistent data",
            )

    if participant_in_db.mess_id:
        mess = await session.execute(
            select(Mess).filter(Mess.id == participant_in_db.mess_id)
        )
        mess = mess.scalar_one()
        if mess is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Inconsistent data",
            )

    return ParticipantResponse(
        name=current_user.name,
        email=current_user.email,
        phone=current_user.phone if current_user.phone else "",
        university=participant_in_db.university,
        accomodation=accomodation.name if accomodation else "No accomodation",
        mess=mess.name if mess else "No mess",
    )


@router.get("/me", response_model=ParticipantResponse, status_code=status.HTTP_200_OK)
async def read_participant_me(
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read current participant"""
    if current_user.role != "participant":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not a participant"
        )
    participant = await session.execute(
        select(Participant).filter(Participant.id == current_user.id)
    )
    participant = participant.scalar_one()
    if participant is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Inconsistent data",
        )

    accomodation, mess = None, None
    if participant.accomodation_id:
        accomodation = await session.execute(
            select(Accomodation).filter(Accomodation.id == participant.accomodation_id)
        )
        accomodation = accomodation.scalar_one()
        if accomodation is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Inconsistent data",
            )

    if participant.mess_id:
        mess = await session.execute(
            select(Mess).filter(Mess.id == participant.mess_id)
        )
        mess = mess.scalar_one()
        if mess is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Inconsistent data",
            )

    return ParticipantResponse(
        name=current_user.name,
        email=current_user.email,
        phone=current_user.phone if current_user.phone else "",
        university=participant.university,
        accomodation=accomodation.name if accomodation else "No accomodation",
        mess=mess.name if mess else "No mess",
    )


# ----------------- Restricted -----------------
@router.get(
    "/all/{event_id}",
    response_model=list[MiniParticipantResponse],
    status_code=status.HTTP_200_OK,
)
async def list_participants(
    event_id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """List all participants"""
    organizers = await session.execute(
        select(Manage).filter(Manage.event_id == event_id)
    )
    organizers = organizers.scalars().all()
    if current_user.role != "admin" and (
        current_user.role != "organizer"
        or current_user.id not in [organizer.id for organizer in organizers]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    
    result = await session.execute(select(Participant))
    participants = result.scalars().all()
    all_participants: list[MiniParticipantResponse] = []
    for participant in participants:
        user = await session.execute(
            select(BaseUser).filter(BaseUser.id == participant.id)
        )
        user = user.scalar_one()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Inconsistent data",
            )
        accomodation, mess = None, None
        if participant.accomodation_id:
            accomodation = await session.execute(
                select(Accomodation).filter(
                    Accomodation.id == participant.accomodation_id
                )
            )
            accomodation = accomodation.scalar_one()
            if accomodation is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inconsistent data",
                )

        if participant.mess_id:
            mess = await session.execute(
                select(Mess).filter(Mess.id == participant.mess_id)
            )
            mess = mess.scalar_one()
            if mess is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inconsistent data",
                )

        all_participants.append(
            MiniParticipantResponse(
                name=user.name,
                email=user.email,
                university=participant.university
            )
        )
    return all_participants

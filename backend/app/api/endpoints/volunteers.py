from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DBAPIError

from app.api import deps
from app.models import Manage, Student, User, Volunteer, Event
from app.schemas.responses import StudentVolunteerResponse, List
from app.schemas.requests import BaseUser, StudentVolunteerRequest


router = APIRouter()


@router.put(
    "/volunteer",
    response_model=StudentVolunteerResponse,
    status_code=status.HTTP_200_OK,
)
async def volunteer_student(
    voulunteer: StudentVolunteerRequest,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Volunteer for an event"""
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not a student"
        )
    student = await session.execute(
        select(Student).filter(Student.id == current_user.id)
    )
    student = student.scalar_one()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Inconsistent data",
        )

    event = await session.execute(select(Event).filter(Event.id == voulunteer.event_id))
    event = event.scalar_one()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    try:
        voulunteer = Volunteer(id=current_user.id, event_id=event.id)
        session.add(voulunteer)
        await session.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already registered as participant",
        )
    except DBAPIError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Already registered as Volunteer",
        )
    return StudentVolunteerResponse(
        name=current_user.name, roll=student.roll, dept=student.dept
    )


# ----------------- Admin -----------------
@router.get(
    "/all/{event_id}",
    response_model=List[StudentVolunteerResponse],
    status_code=status.HTTP_200_OK,
)
async def read_volunteers(
    event_id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read volunteers for an event"""
    organizers = await session.execute(
        select(Manage).filter(Manage.event_id == event_id)
    )
    organizers = organizers.scalars().all()
    volunteers_for_event = await session.execute(
        select(Volunteer, Student, User)
        .join(Student, Volunteer.id == Student.id)
        .join(User, Volunteer.id == User.id)
        .filter(Volunteer.event_id == event_id)
    )
    volunteers_for_event = volunteers_for_event.scalars().all()
    if (
        current_user.role == "admin"
        or (
            current_user.role == "organizer"
            and current_user.id in [organizer.id for organizer in organizers]
        )
        or (
            current_user.role == "student"
            and current_user.id in [volunteer.id for volunteer in volunteers_for_event]
        )
    ):
        volunteers: List[StudentVolunteerResponse] = []
        for volunteer in volunteers_for_event:
            user = await session.execute(select(User).filter(User.id == volunteer.id))
            user = user.scalar_one()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inconsistent data",
                )
            student = await session.execute(
                select(Student).filter(Student.id == volunteer.id)
            )
            student = student.scalar_one()
            if student is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inconsistent data",
                )
            volunteers.append(
                StudentVolunteerResponse(
                    name=user.name, roll=student.roll, dept=student.dept
                )
            )

        return volunteers
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

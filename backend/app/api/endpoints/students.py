from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Student, Volunteer, Event
from app.schemas.responses import List, StudentResponse, StudentVolunteerResponse
from app.schemas.requests import BaseUser, StudentCreateRequest, StudentVolunteerRequest


router = APIRouter()


@router.post("/me", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: StudentCreateRequest,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Create a new student"""
    student = Student(
        id=current_user.id,
        roll=student.roll,
        dept=student.dept,
    )
    session.add(student)
    await session.commit()
    return student


@router.get("/me", response_model=StudentResponse, status_code=status.HTTP_200_OK)
async def read_student_me(
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read current student"""
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
    return student


# ----------------- Admin -----------------
@router.get(
    "/{student_id}", response_model=StudentResponse, status_code=status.HTTP_200_OK
)
async def read_student(
    student_id: str,
    current_user: BaseUser = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read student by id"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin"
        )
    student = await session.execute(select(Student).filter(Student.id == student_id))
    student = student.scalar_one()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return student

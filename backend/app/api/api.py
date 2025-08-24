from fastapi import APIRouter

from app.api.endpoints import auth, users, events, students, volunteers, participants, schedule

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(volunteers.router, prefix="/volunteers", tags=["volunteers"])
api_router.include_router(
    participants.router, prefix="/participants", tags=["participants"]
)
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])

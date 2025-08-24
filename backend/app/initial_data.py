"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if not exists
"""

import asyncio

from sqlalchemy import select, insert, text
from app.models import (
    Accomodation,
    Competition,
    Manage,
    Mess,
    Prize,
    Sponsor,
    Sponsorship,
    User,
    Student,
    Participant,
    Event,
    Venue,
)
import uuid
import hashlib
import datetime

from app.core import config, security
from app.core.session import async_session
from app.models import User
from app.core.security import get_password_hash


user_data = [
    {
        "id": "U001",
        "name": "organizer1",
        "phone": "1001",
        "email": "u1@gmail.com",
        "role": "organizer",
        "password": "1234",
    },
    {
        "id": "U002",
        "name": "organizer2",
        "phone": "1002",
        "email": "u2@gmail.com",
        "role": "organizer",
        "password": "1234",
    },
    {
        "id": "U003",
        "name": "student1",
        "phone": "1003",
        "email": "u3@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U004",
        "name": "organizer3",
        "phone": "1004",
        "email": "u4@gmail.com",
        "role": "organizer",
        "password": "1234",
    },
    {
        "id": "U005",
        "name": "participant1",
        "phone": "1005",
        "email": "u5@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U006",
        "name": "organizer4",
        "phone": "1006",
        "email": "u6@gmail.com",
        "role": "organizer",
        "password": "1234",
    },
    {
        "id": "U007",
        "name": "organizer5",
        "phone": "1007",
        "email": "u7@gmail.com",
        "role": "organizer",
        "password": "1234",
    },
    {
        "id": "U008",
        "name": "student2",
        "phone": "1008",
        "email": "u8@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U009",
        "name": "student3",
        "phone": "1009",
        "email": "u9@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U010",
        "name": "participant2",
        "phone": "1010",
        "email": "u10@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U011",
        "name": "participant3",
        "phone": "1011",
        "email": "u11@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U012",
        "name": "participant4",
        "phone": "1012",
        "email": "u12@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U013",
        "name": "student4",
        "phone": "1013",
        "email": "u13@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U014",
        "name": "student5",
        "phone": "1014",
        "email": "u14@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U015",
        "name": "participant5",
        "phone": "1015",
        "email": "u15@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U016",
        "name": "participant6",
        "phone": "1016",
        "email": "u16@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U017",
        "name": "student6",
        "phone": "1017",
        "email": "u17@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U018",
        "name": "student7",
        "phone": "1018",
        "email": "u18@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U019",
        "name": "participant7",
        "phone": "1019",
        "email": "u19@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U020",
        "name": "participant8",
        "phone": "1020",
        "email": "u20@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U021",
        "name": "participant9",
        "phone": "1021",
        "email": "u21@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U022",
        "name": "participant10",
        "phone": "1022",
        "email": "u22@gmail.com",
        "role": "participant",
        "password": "1234",
    },
    {
        "id": "U023",
        "name": "student8",
        "phone": "1023",
        "email": "u23@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U024",
        "name": "student9",
        "phone": "1024",
        "email": "u24@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U025",
        "name": "student10",
        "phone": "1025",
        "email": "u25@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U026",
        "name": "student11",
        "phone": "1026",
        "email": "u26@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U027",
        "name": "student12",
        "phone": "1027",
        "email": "u27@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U028",
        "name": "student13",
        "phone": "1028",
        "email": "u28@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U029",
        "name": "student14",
        "phone": "1029",
        "email": "u29@gmail.com",
        "role": "student",
        "password": "1234",
    },
    {
        "id": "U030",
        "name": "student15",
        "phone": "1030",
        "email": "u30@gmail.com",
        "role": "student",
        "password": "1234",
    },
]

student_data = [
    {"id": "U003", "roll": "CSE1", "dept": "Computer Science and Engineering"},
    {"id": "U008", "roll": "ECE1", "dept": "Electrical and Electronics Engineering"},
    {"id": "U009", "roll": "EEE1", "dept": "Electrical and Electronics Engineering"},
    {"id": "U013", "roll": "ME1", "dept": "Mechanical Engineering"},
    {"id": "U014", "roll": "CE1", "dept": "Civil Engineering"},
    {"id": "U017", "roll": "CSE2", "dept": "Computer Science and Engineering"},
    {"id": "U018", "roll": "ECE2", "dept": "Electronics and Communication Engineering"},
    {"id": "U023", "roll": "EEE2", "dept": "Electrical and Electronics Engineering"},
    {"id": "U024", "roll": "ME2", "dept": "Mechanical Engineering"},
    {"id": "U025", "roll": "CE2", "dept": "Civil Engineering"},
    {"id": "U026", "roll": "CSE3", "dept": "Computer Science and Engineering"},
    {"id": "U027", "roll": "ECE3", "dept": "Electronics and Communication Engineering"},
    {"id": "U028", "roll": "EEE3", "dept": "Electrical and Electronics Engineering"},
    {"id": "U029", "roll": "ME3", "dept": "Mechanical Engineering"},
    {"id": "U030", "roll": "CE3", "dept": "Civil Engineering"},
]

participant_data = [
    {"id": "U005", "university": "IIT Delhi", "accomodation_id": "A1", "mess_id": "M1"},
    {
        "id": "U010",
        "university": "IIT Guwahati",
        "accomodation_id": "A1",
        "mess_id": "M2",
    },
    {
        "id": "U011",
        "university": "IIT Bombay",
        "accomodation_id": "A2",
        "mess_id": "M2",
    },
    {
        "id": "U012",
        "university": "IIT Bombay",
        "accomodation_id": "A3",
        "mess_id": "M1",
    },
    {"id": "U015", "university": "IIT Delhi", "accomodation_id": "A2", "mess_id": "M3"},
    {
        "id": "U016",
        "university": "IIT Guwahati",
        "accomodation_id": "A3",
        "mess_id": "M2",
    },
    {
        "id": "U019",
        "university": "IIT Madras",
        "accomodation_id": "A2",
        "mess_id": "M1",
    },
    {
        "id": "U020",
        "university": "IIT Kanpur",
        "accomodation_id": "A1",
        "mess_id": "M2",
    },
    {
        "id": "U021",
        "university": "IIT Kanpur",
        "accomodation_id": "A1",
        "mess_id": "M1",
    },
    {
        "id": "U022",
        "university": "IIT Madras",
        "accomodation_id": "A3",
        "mess_id": "M3",
    },
]

venues_data = [
    {"name": "Netaji Auditorium", "location": "Near main building", "capacity": 20},
    {"name": "Takshashila", "location": "Near Nalanda Complex", "capacity": 20},
    {"name": "Vikramshila", "location": "Near Clock Tower", "capacity": 20},
    {"name": "Gymkhana", "location": "Near main building", "capacity": 20},
    {"name": "MG Grounds", "location": "Near Nalanda Complex", "capacity": 20},
]

events_data = [
    {
        "id": "1",
        "name": "Guest Lecture",
        "type": "seminar",
        "desc": "Introductory Seminar by honorable Guest Mr. Sundar Pichai",
        "date": "2024-04-15 10:00:00",
        "duration": "01:00:00",
        "venue": "Netaji Auditorium",
    },
    {
        "id": "2",
        "name": "Overnite",
        "type": "competition",
        "desc": "Competitive Programming Competition held by codeclub",
        "date": "2024-04-15 20:00:00",
        "duration": "20:00:00",
        "venue": "Takshashila",
    },
    {
        "id": "3",
        "name": "Maths Olympiad",
        "type": "competition",
        "desc": "Paper-based mcq test on Maths, Aptitude and Mental Ability",
        "date": "2024-04-16 10:00:00",
        "duration": "02:00:00",
        "venue": "Vikramshila",
    },
    {
        "id": "4",
        "name": "Valorant",
        "type": "competition",
        "desc": "Valorant gaming competition which has to be registered with a team",
        "date": "2024-04-16 19:00:00",
        "duration": "01:30:00",
        "venue": "Gymkhana",
    },
    {
        "id": "5",
        "name": "Musical Concert",
        "type": "concert",
        "desc": "Annual music concert featuring local bands",
        "date": "2024-04-17 20:00:00",
        "duration": "02:00:00",
        "venue": "MG Grounds",
    },
]

manage_data = [
    {'id': 'U001', 'event_id': '1', 'position': 'Head', 'responsibility': 'Overlooks the event'},
    {'id': 'U002', 'event_id': '1', 'position': 'Secretary', 'responsibility': 'Assists the guest lecturer in the event'},
    {'id': 'U004', 'event_id': '1', 'position': 'Secretary', 'responsibility': 'Stage Management'},

    {'id': 'U006', 'event_id': '2', 'position': 'Head', 'responsibility': 'Overlooks the event. Question Framing'},
    {'id': 'U007', 'event_id': '2', 'position': 'Secretary', 'responsibility': 'Invigilation and crowd management'},

    {'id': 'U006', 'event_id': '3', 'position': 'Head', 'responsibility': 'Overlooks the event. Question Framing'},
    {'id': 'U007', 'event_id': '3', 'position': 'Secretary', 'responsibility': 'Invigilation and crowd management'},

    {'id': 'U006', 'event_id': '4', 'position': 'Head', 'responsibility': 'Overlooks the event. Game Design'},
    {'id': 'U007', 'event_id': '4', 'position': 'Secretary', 'responsibility': 'Invigilation and crowd management'},

    {'id': 'U001', 'event_id': '5', 'position': 'Head', 'responsibility': 'Overlooks the event. Relations management'},
    {'id': 'U002', 'event_id': '5', 'position': 'Secretary', 'responsibility': 'Assistance for the guest'},
    {'id': 'U004', 'event_id': '5', 'position': 'Secretary', 'responsibility': 'Stage Management'},

]

competitions_data = [
    {"id": "2", "props": "Computers,Chairs,Papers,Pens"},
    {"id": "3", "props": "Papers,Pens,Chairs"},
    {"id": "4", "props": "Headphones,Internet,Chairs"},
]

sponsors_data = [
    {"id": "1", "name": "Sony", "desc": "Electronics and entertainment company."},
    {"id": "2", "name": "Apple", "desc": "Multinational technology company."},
    {
        "id": "3",
        "name": "Google",
        "desc": "Multinational technology company specializing in internet-related services.",
    },
    {
        "id": "4",
        "name": "Riot Games",
        "desc": "Video game developer and esports tournament organizer.",
    },
    {
        "id": "5",
        "name": "Samsung",
        "desc": "Multinational Android device manufacturer.",
    },
]

sponsorships_data = [
    {"sponsor_id": "1", "event_id": "5", "amount": 50000},
    {"sponsor_id": "2", "event_id": "2", "amount": 50000},
    {"sponsor_id": "3", "event_id": "1", "amount": 50000},
    {"sponsor_id": "4", "event_id": "4", "amount": 50000},
    {"sponsor_id": "5", "event_id": "3", "amount": 50000},
]

prizes_data = [
    {"event_id": "2", "position": 1, "amount": 20000, "winner_id": None},
    {"event_id": "2", "position": 2, "amount": 15000, "winner_id": None},
    {"event_id": "2", "position": 3, "amount": 10000, "winner_id": None},
    {"event_id": "3", "position": 1, "amount": 30000, "winner_id": None},
    {"event_id": "3", "position": 2, "amount": 25000, "winner_id": None},
    {"event_id": "3", "position": 3, "amount": 20000, "winner_id": None},
    {"event_id": "3", "position": 3, "amount": 15000, "winner_id": None},
    {"event_id": "3", "position": 3, "amount": 10000, "winner_id": None},
    {"event_id": "4", "position": 1, "amount": 10000, "winner_id": None},
    {"event_id": "4", "position": 2, "amount": 7000, "winner_id": None},
    {"event_id": "4", "position": 3, "amount": 5000, "winner_id": None}
]

messes_data = [
    {"id": "M1", "name": "Mess1", "location": "Takshashila", "capacity": 20},
    {"id": "M2", "name": "Mess2", "location": "Gymkhana", "capacity": 20},
    {"id": "M3", "name": "Mess3", "location": "MG Grounds", "capacity": 20},
]

accomodations_data = [
    {"id": "A1", "name": "Accomodation1", "location": "VS Hall", "capacity": 30},
    {"id": "A2", "name": "Accomodation2", "location": "RP Hall", "capacity": 30},
    {"id": "A3", "name": "Accomodation3", "location": "RK Hall", "capacity": 30},
]


# ------------------------- Populate Data -------------------------
ID_EXTENDER = "00000000-0000-0000-0000-0000000"


def convert_to_uuid(string):
    return uuid.UUID(hex=hashlib.md5((ID_EXTENDER + string).encode()).hexdigest())


async def populate_data(session):
    async with session.begin():
        for user in user_data:
            user["id"] = convert_to_uuid(user["id"])
            user["password"] = get_password_hash(user["password"])
            await session.execute(insert(User).values(user))
        for student in student_data:
            student["id"] = convert_to_uuid(student["id"])
            await session.execute(insert(Student).values(student))
        for mess in messes_data:
            mess["id"] = convert_to_uuid(mess["id"])
            await session.execute(insert(Mess).values(mess))
        for accomodation in accomodations_data:
            accomodation["id"] = convert_to_uuid(accomodation["id"])
            await session.execute(insert(Accomodation).values(accomodation))
        for participant in participant_data:
            participant["id"] = convert_to_uuid(participant["id"])
            participant["accomodation_id"] = convert_to_uuid(
                participant["accomodation_id"]
            )
            participant["mess_id"] = convert_to_uuid(participant["mess_id"])
            await session.execute(insert(Participant).values(participant))
        for venue in venues_data:
            await session.execute(insert(Venue).values(venue))
        for event in events_data:
            event["id"] = convert_to_uuid(event["id"])
            event["date"] = datetime.datetime.strptime(
                event["date"], "%Y-%m-%d %H:%M:%S"
            )
            event["duration"] = datetime.timedelta(
                hours=int(event["duration"].split(":")[0]),
                minutes=int(event["duration"].split(":")[1]),
                seconds=int(event["duration"].split(":")[2]),
            )
            await session.execute(insert(Event).values(event))
        for manage in manage_data:
            manage["id"] = convert_to_uuid(manage["id"])
            manage["event_id"] = convert_to_uuid(manage["event_id"])
            await session.execute(insert(Manage).values(manage))
        for competition in competitions_data:
            competition["id"] = convert_to_uuid(competition["id"])
            await session.execute(insert(Competition).values(competition))
        for sponsor in sponsors_data:
            sponsor["id"] = convert_to_uuid(sponsor["id"])
            await session.execute(insert(Sponsor).values(sponsor))
        for sponsorship in sponsorships_data:
            sponsorship["sponsor_id"] = convert_to_uuid(sponsorship["sponsor_id"])
            sponsorship["event_id"] = convert_to_uuid(sponsorship["event_id"])
            await session.execute(insert(Sponsorship).values(sponsorship))
        for prize in prizes_data:
            prize["event_id"] = convert_to_uuid(prize["event_id"])
            prize["winner_id"] = (
                convert_to_uuid(prize["winner_id"]) if prize["winner_id"] else None
            )
            await session.execute(insert(Prize).values(prize))


# ------------------------- Create Triggers -------------------------
async def create_triggers(session):
    async with session.begin():
        await session.execute(text(
            """
            CREATE OR REPLACE FUNCTION reg_check()
            RETURNS TRIGGER AS $$
            DECLARE
            acid UUID;
            ac_avail INTEGER;
            mid UUID;
            m_avail INTEGER;
            BEGIN
            select id,capacity into acid,ac_avail from accomodation order by capacity desc limit 1;
            select id,capacity into mid,m_avail from mess order by capacity desc limit 1;
            IF (ac_avail = 0) THEN
                acid = NULL;
            END IF;

            IF m_avail=0 THEN
                mid = NULL;
            END IF;

            UPDATE accomodation SET capacity = capacity - 1 WHERE id = acid;
            UPDATE mess SET capacity = capacity - 1 WHERE id = mid;
            NEW.mess_id = mid;
            NEW.accomodation_id = acid;
            
            RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            
            """)
        )
        await session.execute(text(
            """

            CREATE TRIGGER reg_check_trigger
            BEFORE INSERT ON participant
            FOR EACH ROW
            EXECUTE FUNCTION reg_check();
            """)
        )
        await session.execute(text(
            """

            CREATE OR REPLACE FUNCTION stu_as_vol_check()
            RETURNS TRIGGER AS $$
            DECLARE
            cnt INTEGER DEFAULT 0;
            BEGIN
            SELECT COUNT(user_id) INTO cnt
            FROM registration
            WHERE registration.user_id = NEW.id AND registration.event_id = NEW.event_id;
            IF cnt <> 0 THEN
                RAISE EXCEPTION 'Already registered as participant for this event';
            END IF;
            RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """)
        )
        await session.execute(text(
            """
            CREATE TRIGGER stu_as_vol_trigger 
            BEFORE INSERT ON volunteer
            FOR EACH ROW
            EXECUTE FUNCTION stu_as_vol_check();
            """)
        )
        await session.execute(text(
            """
            CREATE OR REPLACE FUNCTION vol_as_par_check()
            RETURNS TRIGGER AS $$
            DECLARE 
            cnt INTEGER DEFAULT 0;
            BEGIN
            SELECT COUNT(id) INTO cnt
            FROM volunteer
            WHERE volunteer.event_id = NEW.event_id and volunteer.id = NEW.user_id;
            IF cnt <> 0 THEN
                RAISE EXCEPTION 'Already registered as volunteer for this event';
            END IF;
            RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """)
        )
        await session.execute(text(
            """
            --- VOLUNTEER IS NOT ALLOWED TO PARTICIPATE IN HIS EVENT 
            CREATE TRIGGER vol_as_par_trigger
            BEFORE INSERT ON registration
            FOR EACH ROW
            EXECUTE FUNCTION vol_as_par_check();

            """)
        )


async def main() -> None:
    print("Start initial data")
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.email == config.settings.FIRST_SUPERUSER_EMAIL)
        )
        user = result.scalars().first()

        if user is None:
            new_superuser = User(
                email=config.settings.FIRST_SUPERUSER_EMAIL,
                name="admin",
                role="admin",
                password=get_password_hash(config.settings.FIRST_SUPERUSER_PASSWORD),
                phone="1234567890",
            )
            session.add(new_superuser)
            await session.commit()
            print("Admin was created")
        else:
            print("Admin already exists in database")

    async with async_session() as session:
        await populate_data(session)
        await session.commit()
        print("Data populated")

    print("Initial data created")

    async with async_session() as session:
        await create_triggers(session)
        await session.commit()
        print("Triggers created")


if __name__ == "__main__":
    asyncio.run(main())

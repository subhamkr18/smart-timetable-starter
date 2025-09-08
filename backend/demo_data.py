# backend/demo_data.py
from .auth import get_password_hash

def get_demo_state():
    return {
        "users": [
            {
                "username": "admin",
                "hashed_password": get_password_hash("admin"),  # ✅ fixed
                "role": "admin",
            },
            {
                "username": "faculty1",
                "hashed_password": get_password_hash("faculty1"),  # ✅ fixed
                "role": "faculty",
            },
            {
                "username": "student1",
                "hashed_password": get_password_hash("student1"),  # ✅ fixed
                "role": "student",
            },
        ],
        "config": {
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "periods_per_day": 6
        },
        "rooms": [
            {"name": "Room 101", "capacity": 60, "type": "classroom"},
            {"name": "Room 102", "capacity": 40, "type": "classroom"},
            {"name": "Lab 1", "capacity": 30, "type": "lab"},
        ],
        "teachers": [
            {"name": "Dr. Smith", "code": "T1", "max_load": 10, "avail_periods": []},
            {"name": "Prof. Johnson", "code": "T2", "max_load": 8, "avail_periods": []},
            {"name": "Ms. Lee", "code": "T3", "max_load": 12, "avail_periods": []},
        ],
        "batches": [
            {"name": "CSE-A", "size": 50, "semester": 3, "max_per_day": 4},
            {"name": "CSE-B", "size": 45, "semester": 3, "max_per_day": 4},
        ],
        "subjects": [
            {"name": "Data Structures", "code": "S1", "batch": "CSE-A",
             "teacher_code": "T1", "classes_per_week": 3, "duration": 1, "fixed_slots": None},
            {"name": "Algorithms", "code": "S2", "batch": "CSE-A",
             "teacher_code": "T2", "classes_per_week": 2, "duration": 1, "fixed_slots": None},
            {"name": "Operating Systems", "code": "S3", "batch": "CSE-B",
             "teacher_code": "T1", "classes_per_week": 3, "duration": 1, "fixed_slots": None},
            {"name": "DBMS", "code": "S4", "batch": "CSE-B",
             "teacher_code": "T3", "classes_per_week": 2, "duration": 1, "fixed_slots": None},
        ],
        "latest_timetable": []
    }

# backend/timetable.py
from fastapi import APIRouter, Depends
from .auth import get_current_user
from . import storage

router = APIRouter(prefix="/timetable", tags=["timetable"])

# ✅ generate timetable (dummy for demo)
@router.post("/generate")
def generate_timetable(user: dict = Depends(get_current_user)):
    # get stored teachers/rooms/batches (demo only)
    teachers = storage.get_state().get("teachers", [])
    rooms = storage.get_state().get("rooms", [])
    batches = storage.get_state().get("batches", [])

    timetable = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

    period = 1
    for day in days:
        for teacher in teachers:
            timetable.append({
                "day": day,
                "period": period,
                "teacher": teacher["name"],
                "room": rooms[period % len(rooms)]["name"] if rooms else "Room A",
                "batch": batches[period % len(batches)]["name"] if batches else "Batch X"
            })
            period += 1

    storage.set_state("timetable", timetable)
    return {"status": "generated", "timetable": timetable}

# ✅ get latest timetable
@router.get("/latest")
def get_latest_timetable(user: dict = Depends(get_current_user)):
    return storage.get_state().get("timetable", [])

# backend/subjects.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from . import storage
from .auth import get_current_user

router = APIRouter(prefix="/subjects", tags=["subjects"])

class Subject(BaseModel):
    name: str
    faculty: str = None   # username of assigned faculty (optional)


# ✅ Get all subjects
@router.get("/", response_model=List[Subject])
def get_subjects(current_user: dict = Depends(get_current_user)):
    return storage.get_state().get("subjects", [])


# ✅ Add subject (admin only)
@router.post("/", response_model=Subject)
def add_subject(subject: Subject, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    state = storage.get_state()
    subjects = state.get("subjects", [])
    if any(s["name"] == subject.name for s in subjects):
        raise HTTPException(status_code=400, detail="Subject already exists")

    subjects.append(subject.dict())
    storage.set_state(state)
    return subject


# ✅ Assign subject to faculty
@router.put("/{name}", response_model=Subject)
def assign_subject(name: str, faculty: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    state = storage.get_state()
    subjects = state.get("subjects", [])

    for subj in subjects:
        if subj["name"] == name:
            subj["faculty"] = faculty
            storage.set_state(state)
            return subj

    raise HTTPException(status_code=404, detail="Subject not found")


# ✅ Delete subject
@router.delete("/{name}")
def delete_subject(name: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    state = storage.get_state()
    subjects = state.get("subjects", [])
    new_subjects = [s for s in subjects if s["name"] != name]

    if len(new_subjects) == len(subjects):
        raise HTTPException(status_code=404, detail="Subject not found")

    state["subjects"] = new_subjects
    storage.set_state(state)
    return {"msg": f"Subject {name} deleted successfully"}

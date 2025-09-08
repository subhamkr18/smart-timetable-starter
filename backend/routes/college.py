from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/college", tags=["College"])

# In-memory storage (replace later with DB)
college_config = {
    "classDuration": 50,
    "numClassrooms": 10,
    "numFaculties": 20,
    "batches": ["2022", "2023"],
    "branches": ["CSE", "ECE"],
    "subjects": ["Math", "Physics", "Programming"],
    "labsPerSubject": [],
    "labDuration": 120,
    "facultyHolidays": 2,
    "avoidCollisions": False,
}

class CollegeConfig(BaseModel):
    classDuration: int
    numClassrooms: int
    numFaculties: int
    batches: List[str]
    branches: List[str]
    subjects: List[str]
    labsPerSubject: List[str]
    labDuration: int
    facultyHolidays: int
    avoidCollisions: bool

@router.get("/config")
def get_config():
    return college_config

@router.post("/config")
def save_config(config: CollegeConfig):
    global college_config
    college_config = config.dict()
    return college_config

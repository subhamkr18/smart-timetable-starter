# backend/models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# ------------------------
# Types
# ------------------------
Day = Literal["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
RoomType = Literal["classroom", "lab", "smart"]
RoleType = Literal["admin", "faculty", "student"]

# ------------------------
# Models
# ------------------------
class Room(BaseModel):
    name: str
    capacity: int = Field(ge=1)
    type: RoomType = "classroom"


class Teacher(BaseModel):
    name: str
    code: str
    max_load: int = Field(ge=0)  # periods/week
    avail_periods: List[int] = Field(default_factory=list)  # allowed period numbers in a day


class Subject(BaseModel):
    name: str
    code: str
    batch: str                # which batch/group takes it
    teacher_code: str
    classes_per_week: int = Field(ge=1)
    duration: int = 1
    fixed_slots: Optional[List[str]] = None  # e.g. ["Mon-3","Wed-5"]


class Batch(BaseModel):
    name: str
    size: int = Field(ge=1)
    semester: int = 1
    max_per_day: int = 6


class Branch(BaseModel):
    name: str


class Config(BaseModel):
    days: List[Day] = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    periods_per_day: int = 8


# ------------------------
# User & Auth Models
# ------------------------
class User(BaseModel):
    username: str
    password: str
    role: RoleType


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

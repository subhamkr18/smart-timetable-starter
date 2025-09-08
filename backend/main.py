# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from . import models, storage, demo_data, scheduler
from .auth import router as auth_router, get_current_user, get_password_hash

# ------------------- Lifespan -------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        storage.ensure_passwords_hashed()
        _create_default_admin()
        print("🚀 Backend ready")
    except Exception as e:
        print("WARNING: Startup issue...", e)
    yield


app = FastAPI(
    title="Smart Timetable API",
    version="2.5",
    description="Backend for Smart Timetable project with JWT Auth and timetable generation",
    lifespan=lifespan,   # ✅ modern lifespan usage
)

# ------------------- Middleware -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Auth Router -------------------
app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running 🚀"}


@app.get("/health")
def health():
    return {"ok": True}


# ------------------- Reset & Seed -------------------

@app.post("/reset")
def reset(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can reset data")
    storage.reset_state()
    _create_default_admin()
    return {"status": "reset"}


@app.post("/reset-open")
def reset_open():
    """Dangerous: open reset for testing only."""
    storage.reset_state()
    _create_default_admin()
    return {"status": "reset (open) — remove in production!"}


@app.post("/seed-demo")
def seed_demo():
    state = demo_data.get_demo_state()
    s = storage.get_state()
    s.clear()
    s.update(state)
    storage.save_state(s)
    _create_default_admin()
    return {"status": "demo data loaded"}


# ------------------- CRUD Endpoints -------------------

@app.get("/state")
def get_state(current_user: dict = Depends(get_current_user)):
    return storage.get_state()


@app.post("/rooms")
def add_room(room: models.Room, current_user: dict = Depends(get_current_user)):
    s = storage.get_state()
    s.setdefault("rooms", []).append(room.dict())
    storage.save_state(s)
    return {"status": "room added"}


@app.post("/teachers")
def add_teacher(t: models.Teacher, current_user: dict = Depends(get_current_user)):
    s = storage.get_state()
    s.setdefault("teachers", []).append(t.dict())
    storage.save_state(s)
    return {"status": "teacher added"}


@app.post("/subjects")
def add_subject(subj: models.Subject, current_user: dict = Depends(get_current_user)):
    s = storage.get_state()
    s.setdefault("subjects", []).append(subj.dict())
    storage.save_state(s)
    return {"status": "subject added"}


@app.post("/batches")
def add_batch(b: models.Batch, current_user: dict = Depends(get_current_user)):
    s = storage.get_state()
    s.setdefault("batches", []).append(b.dict())
    storage.save_state(s)
    return {"status": "batch added"}


@app.post("/branches")
def add_branch(b: models.Branch, current_user: dict = Depends(get_current_user)):
    s = storage.get_state()
    s.setdefault("branches", []).append(b.dict())
    storage.save_state(s)
    return {"status": "branch added"}


@app.post("/config")
def update_config(cfg: models.Config, current_user: dict = Depends(get_current_user)):
    s = storage.get_state()
    s["config"] = cfg.dict()
    storage.save_state(s)
    return {"status": "config updated"}


# ------------------- College Config -------------------

@app.get("/college/config")
def get_college_config(current_user: dict = Depends(get_current_user)):
    """Return available batches, branches and subjects for dropdowns."""
    s = storage.get_state()
    return {
        "batches": [b.get("name") for b in s.get("batches", [])],
        "branches": [br.get("name") for br in s.get("branches", [])],
        "subjects": [sub.get("name") for sub in s.get("subjects", [])],
    }



# ------------------- Classroom & Faculty -------------------

@app.get("/classrooms")
def get_classrooms(current_user: dict = Depends(get_current_user)):
    s = storage.get_state()
    return s.get("rooms", [])


@app.get("/auth/faculty")
def get_faculty_profile(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "faculty":
        raise HTTPException(status_code=403, detail="Only faculty can access this")
    return current_user


# ------------------- Timetable Generation -------------------

class PeriodDef(BaseModel):
    name: str
    start: str
    end: str
    is_lunch: Optional[bool] = False


class GenerateRequest(BaseModel):
    batches: Optional[List[str]] = None
    branches: Optional[List[str]] = None
    subjects: Optional[List[str]] = None
    periods: Optional[List[PeriodDef]] = None


def _compute_periods_from_config(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    def parse_hhmm(t: str) -> int:
        try:
            h, m = t.split(":")
            return int(h) * 60 + int(m)
        except Exception:
            return 9 * 60  # default 09:00

    start_time = cfg.get("start_time", "09:00")
    end_time = cfg.get("end_time", "16:00")
    per_len = int(cfg.get("period_length_minutes", 50))
    lunch_after = int(cfg.get("lunch_after_period", 3))

    start_min = parse_hhmm(start_time)
    end_min = parse_hhmm(end_time)

    periods = []
    idx = 1
    cur = start_min
    while cur + per_len <= end_min:
        s_h, s_m = divmod(cur, 60)
        e_h, e_m = divmod(cur + per_len, 60)
        slot = {
            "name": f"Period {idx}",
            "start": f"{s_h:02d}:{s_m:02d}",
            "end": f"{e_h:02d}:{e_m:02d}",
            "is_lunch": False,
        }
        if idx == lunch_after + 1:
            slot["name"] = "Lunch"
            slot["is_lunch"] = True
        periods.append(slot)
        cur += per_len
        idx += 1

    return periods


def _build_solver_state(state: dict, req: Optional[GenerateRequest] = None) -> dict:
    config = state.get("config", {}) or {}
    rooms = state.get("rooms", []) or []
    teachers = state.get("teachers", []) or []
    subjects = state.get("subjects", []) or []
    batches = state.get("batches", []) or []
    branches = state.get("branches", []) or []

    if req:
        if req.batches:
            batches = [b for b in batches if b.get("name") in set(req.batches)]
        if req.branches:
            sel_branches = set(req.branches)
            subjects = [s for s in subjects if s.get("branch") in sel_branches or not s.get("branch")]
        if req.subjects:
            sel_subs = set(req.subjects)
            subjects = [s for s in subjects if s.get("name") in sel_subs]

    batch_dict = {b["name"]: b for b in batches if "name" in b}

    periods_from_req = [p.dict() for p in (req.periods or [])]
    periods_from_cfg = config.get("periods") or []
    periods = periods_from_req or periods_from_cfg or _compute_periods_from_config(config)

    solver_config = {
        "days": config.get("days", ["Mon", "Tue", "Wed", "Thu", "Fri"]),
        "periods_per_day": int(config.get("periods_per_day", len(periods) or 6)),
        "periods": periods,
        "lab_length_minutes": int(config.get("lab_length_minutes", 100)),
    }

    return {
        "config": solver_config,
        "rooms": rooms,
        "teachers": teachers,
        "subjects": subjects,
        "batches": batch_dict,
        "branches": branches,
    }


def _call_scheduler(solver_state: dict, seed: int | None = None):
    try:
        return scheduler.make_timetable(solver_state, seed=seed)  # type: ignore
    except TypeError:
        return scheduler.make_timetable(solver_state)


def _generate_candidates(solver_state: dict, n: int = 3):
    candidates = []
    for i in range(n):
        result = _call_scheduler(solver_state, seed=i)
        candidates.append(result)
    return candidates


@app.post("/timetable/generate")
def generate_timetable(req: GenerateRequest, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "faculty"]:
        raise HTTPException(status_code=403, detail="Only admin/faculty can generate timetable")

    state = storage.get_state()
    solver_state = _build_solver_state(state, req)

    try:
        candidates = _generate_candidates(solver_state, n=3)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except RuntimeError as e:
        raise HTTPException(409, str(e))

    state["timetable_candidates"] = candidates
    storage.save_state(state)
    return {"status": "candidates_generated", "count": len(candidates), "candidates": candidates}


@app.post("/timetable/finalize")
def finalize_timetable(choice: dict, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can finalize timetable")

    state = storage.get_state()
    candidates = state.get("timetable_candidates", [])
    if not candidates:
        raise HTTPException(404, detail="No timetable candidates available. Generate first.")

    idx = int(choice.get("choice", 0))
    if idx < 0 or idx >= len(candidates):
        raise HTTPException(400, detail=f"Invalid choice index {idx}")

    state["latest_timetable"] = candidates[idx]
    storage.save_state(state)
    return {"status": "finalized", "chosen_index": idx}


@app.get("/timetable/latest")
def get_latest_timetable(current_user: dict = Depends(get_current_user)):
    return storage.get_state().get("latest_timetable", [])


# ---- Compatibility Aliases ----

@app.post("/schedule/generate")
def schedule_generate_alias(req: GenerateRequest, current_user: dict = Depends(get_current_user)):
    return generate_timetable(req, current_user)  # type: ignore


@app.post("/timetable/select")
def timetable_select_alias(index: int = Query(0), current_user: dict = Depends(get_current_user)):
    return finalize_timetable({"choice": index}, current_user)  # type: ignore


@app.get("/timetable")
def timetable_get_alias(current_user: dict = Depends(get_current_user)):
    return get_latest_timetable(current_user)


# ------------------- Default Admin -------------------

def _create_default_admin():
    s = storage.get_state()
    users = s.get("users", [])
    if not any(u.get("username") == "admin" for u in users):
        admin_user = {
            "username": "admin",
            "hashed_password": get_password_hash("admin123"),
            "role": "admin",
            "name": "Super Admin",
        }
        users.append(admin_user)
        s["users"] = users
        storage.save_state(s)  # ✅ pass state explicitly
        print("✅ Default admin created: username=admin, password=admin123")
    else:
        "INFO: Admin already exists"
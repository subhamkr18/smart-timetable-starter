# backend/schedulerapi.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, List, Any
from . import storage
from .auth import get_current_user
from .solver import make_timetable

router = APIRouter(tags=["scheduler"])

def slug(s: str) -> str:
    return "".join(ch.lower() for ch in s if ch.isalnum() or ch in ("-", "_"))

def _build_solver_state(app_state: Dict[str, Any], batch: str | None = None, branch: str | None = None, subjects: List[str] | None = None) -> Dict[str, Any]:
    """
    Build solver state from global app state, filtered by batch/branch/subjects if provided.
    """

    config = app_state.get("config") or app_state.get("college_config") or {}
    days = config.get("days") or ["Mon", "Tue", "Wed", "Thu", "Fri"]
    periods_per_day = int(config.get("periods_per_day", config.get("P", 6)))

    # --- Rooms ---
    rooms_src = app_state.get("rooms") or app_state.get("classrooms") or []
    rooms = [{"name": r.get("name") or f"Room-{i+1}", "capacity": int(r.get("capacity", 40))} for i, r in enumerate(rooms_src)]
    if not rooms:
        raise HTTPException(400, "No rooms/classrooms found")

    # --- Teachers ---
    teachers_src = app_state.get("teachers") or app_state.get("faculties") or []
    teachers = []
    for t in teachers_src:
        code = t.get("code") or f"T{t.get('id','') or slug(t.get('name',''))}"
        teachers.append({
            "code": code,
            "name": t.get("name", code),
            "max_load": int(t.get("max_load", 16)),
            "avail_periods": t.get("avail_periods", []),
        })
    if not teachers:
        raise HTTPException(400, "No teachers/faculties found")
    teacher_codes = {t["code"] for t in teachers}

    # --- Subjects ---
    subjects_src = app_state.get("subjects") or []
    selected_subjects = []
    batches_dict: Dict[str, Dict[str, Any]] = {}

    for s in subjects_src:
        s_name = s.get("name") or s.get("subject")
        s_batch = s.get("batch")
        s_branch = s.get("branch")

        # filter
        if batch and s_batch != batch:
            continue
        if branch and s_branch != branch:
            continue
        if subjects and s_name not in subjects:
            continue

        tcode = s.get("teacher_code")
        if not tcode or tcode not in teacher_codes:
            tcode = next(iter(teacher_codes))

        selected_subjects.append({
            "name": s_name,
            "code": s.get("code") or slug(s_name),
            "teacher_code": tcode,
            "batch": s_batch,
            "classes_per_week": int(s.get("classes_per_week", 2)),
            "fixed_slots": s.get("fixed_slots", []),
        })

        if s_batch not in batches_dict:
            batches_dict[s_batch] = {
                "name": s_batch,
                "size": int(s.get("batch_size", 60)),
                "max_per_day": int(s.get("batch_max_per_day", 5)),
            }

    if not selected_subjects:
        raise HTTPException(400, "No subjects found for given filter")

    return {
        "config": {"days": days, "periods_per_day": periods_per_day},
        "rooms": rooms,
        "teachers": teachers,
        "subjects": selected_subjects,
        "batches": batches_dict,
    }

@router.post("/schedule/generate")
def generate_schedule(
    batch: str | None = None,
    branch: str | None = None,
    subjects: List[str] | None = None,
    current_user: Dict = Depends(get_current_user),
):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Only admin can generate timetable")

    state = storage.get_state()
    solver_state = _build_solver_state(state, batch=batch, branch=branch, subjects=subjects)

    # generate multiple candidates
    candidates = []
    for i in range(3):  # generate 3 variations
        try:
            result = make_timetable(solver_state)
            candidates.append(result)
        except Exception as e:
            raise HTTPException(400, f"Solver failed: {e}")

    # store temporarily for selection
    state["timetable_candidates"] = candidates
    storage.set_state(state)

    return {"message": "✅ Candidates generated", "count": len(candidates), "candidates": candidates}

@router.post("/timetable/select")
def select_timetable(index: int, current_user: Dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Only admin can select timetable")

    state = storage.get_state()
    candidates = state.get("timetable_candidates")
    if not candidates:
        raise HTTPException(404, "No generated timetables available")

    if index < 0 or index >= len(candidates):
        raise HTTPException(400, "Invalid index")

    state["timetable"] = candidates[index]
    storage.set_state(state)
    return {"message": f"✅ Timetable {index} selected and saved"}

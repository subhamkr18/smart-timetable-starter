# Smart Timetable Starter (FastAPI + OR-Tools)

This is a minimal, beginner-friendly starter to generate optimized class timetables.

## What you get
- **Backend**: Python FastAPI + Google OR-Tools (CP-SAT) solver.
- **Frontend**: Simple HTML+JS page served by FastAPI.
- **Sample data** endpoint so you can test instantly.

## Quick Start

1. **Install Python 3.10+** (Windows/Mac/Linux).
2. Open a terminal in this folder (where this README is).
3. Create and activate a virtual environment:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux (bash/zsh):
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
5. Run the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
6. Open your browser at **http://127.0.0.1:8000/**  
   - Click **Load Sample** → **Generate Timetable**.

## How it works (high level)
- You send a JSON **problem** to `POST /api/optimize`:
  - `days`, `slots_per_day`
  - `rooms` (capacity, type, attributes)
  - `faculty` (eligible courses, unavailability)
  - `classes` (batch_id, size, weekly count, eligible rooms/faculty, duration in slots)
  - optional `fixed_events` (block specific day/slot for a room/faculty/batch)
- The solver places each class **instance** exactly once while avoiding collisions across **room**, **faculty**, and **batch**.
- A small **soft penalty** prefers avoiding the **last slot** of the day.
- You get a `timetable_by_batch` grid in the response.

## Customize (next steps)
- Add more soft constraints in `backend/main.py` (search for `# Soft penalty`). For example:
  - Penalize >2 consecutive slots for the same batch/faculty.
  - Prefer spreading a course across different days.
  - Respect preferred days/slots per course/faculty.
- Add **max_per_day** and **max_week** constraints (currently fields exist but not enforced).
- Add **multi-department** by giving batches unique IDs and adding more rooms/faculty.
- Add **multi-shift** by splitting `days/slots` per shift or by blocking slots via `fixed_events`.

## API
- `GET /api/sample` → returns editable sample JSON
- `POST /api/optimize` → body = ProblemInput JSON (see `/api/sample` for shape)

## Deploy
- Keep running with `uvicorn ...` for development.
- For production, consider: `gunicorn -k uvicorn.workers.UvicornWorker backend.main:app` behind Nginx.

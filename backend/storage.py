import json
from pathlib import Path
import bcrypt

DATA_FILE = Path(__file__).parent / "data.json"

def get_state() -> dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Corrupted data.json, resetting...")
            reset_state()
            return get_state()
    return {}

def save_state(state: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(state, f, indent=2)

def reset_state():
    state = {
        "users": [],
        "config": {},
        "rooms": [],
        "teachers": [],
        "batches": [],
        "subjects": [],
        "latest_timetable": []
    }
    save_state(state)

def ensure_passwords_hashed():
    """
    Make sure all users in data.json have bcrypt-hashed passwords.
    If they are plain text, hash them and update file.
    """
    if not DATA_FILE.exists():
        return

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Corrupted data.json, skipping password check.")
        return

    changed = False
    for user in data.get("users", []):
        pwd = user.get("hashed_password")
        if pwd and not str(pwd).startswith("$2b$"):
            hashed = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user["hashed_password"] = hashed
            changed = True
            print(f"🔐 Hashed password for user: {user['username']}")

    if changed:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("✅ Updated data.json with secure password hashes")

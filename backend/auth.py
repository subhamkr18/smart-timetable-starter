# backend/auth.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from . import storage

# --- Config ---
SECRET_KEY = "replace-this-with-a-secret-key"  # 🔐 change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------- Models ----------------
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None

class FacultyCreate(BaseModel):
    username: str
    password: str

class FacultyUpdate(BaseModel):
    new_password: str

# ---------------- Utils ----------------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    users = storage.get_state().get("users", [])

    # ✅ Hardcode default admin if none exists
    if not any(u["role"] == "admin" for u in users):
        default_admin = {
            "username": "admin",
            "hashed_password": get_password_hash("admin"),  # username=admin, password=admin
            "role": "admin",
        }
        users.append(default_admin)
        storage.set_state({"users": users})

    for u in users:
        if u["username"] == username and verify_password(password, u["hashed_password"]):
            return u
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    users = storage.get_state().get("users", [])
    for u in users:
        if u["username"] == username:
            return u
    raise credentials_exception

# ---------------- Routes ----------------
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

# ✅ Current logged-in user
@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "role": current_user["role"]}

# ✅ Admin creates faculty accounts
@router.post("/register/faculty")
def register_faculty(data: FacultyCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    users = storage.get_state().get("users", [])
    if any(u["username"] == data.username for u in users):
        raise HTTPException(status_code=400, detail="Username already exists")

    new_faculty = {
        "username": data.username,
        "hashed_password": get_password_hash(data.password),
        "role": "faculty",
    }
    users.append(new_faculty)
    storage.set_state({"users": users})

    return {"msg": "Faculty registered successfully", "username": data.username}

# ✅ Admin lists all faculty
@router.get("/faculty")
def list_faculty(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    users = storage.get_state().get("users", [])
    return [u for u in users if u["role"] == "faculty"]

# ✅ Admin updates faculty password
@router.put("/faculty/{username}")
def update_faculty(username: str, data: FacultyUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    state = storage.get_state()
    users = state.get("users", [])
    for u in users:
        if u["username"] == username and u["role"] == "faculty":
            u["hashed_password"] = get_password_hash(data.new_password)
            storage.set_state({"users": users})
            return {"msg": "Faculty password updated", "username": username}

    raise HTTPException(status_code=404, detail="Faculty not found")

# ✅ Admin deletes faculty
@router.delete("/faculty/{username}")
def delete_faculty(username: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    state = storage.get_state()
    users = state.get("users", [])
    new_users = [u for u in users if not (u["username"] == username and u["role"] == "faculty")]

    if len(new_users) == len(users):
        raise HTTPException(status_code=404, detail="Faculty not found")

    storage.set_state({"users": new_users})
    return {"msg": f"Faculty {username} deleted successfully"}

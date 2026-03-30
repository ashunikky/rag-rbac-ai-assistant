# app/auth/auth.py

from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import SECRET_KEY

# ---------------- USERS ----------------
USERS = {
    "ashutosh": {"password": "123", "role": "c_level"},
    "ravi": {"password": "123", "role": "finance"},
    "sunita": {"password": "123", "role": "hr"},
    "rohit": {"password": "123", "role": "engineering"},
    "priya": {"password": "123", "role": "marketing"},
    "raj": {"password": "123", "role": "employee"}
}

# ---------------- JWT CONFIG ----------------
ALGORITHM = "HS256"

# ---------------- CREATE TOKEN ----------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------- AUTH DEPENDENCY ----------------
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
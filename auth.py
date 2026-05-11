from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import uuid, os, hashlib
from db import get_db
from models import User, RefreshToken

ACCESS_TIME_MIN = 15
REFRESH_TIME_DAY = 7

SECURITY_KEY= os.getenv("SECURITY_KEY")
if not SECURITY_KEY:
    raise ValueError("dev-secret env var not set")
ALGORITHM = "HS256"

pwd = CryptContext(schemes=['bcrypt'])

def hash_password(password: str):
    return pwd.hash(password[:72])

def verify_password(plain, hashed):
    return pwd.verify(plain, hashed)

def create_access_token(user_id: str):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TIME_MIN)
    }
    return jwt.encode(payload, SECURITY_KEY, algorithm=ALGORITHM)

def hash_refresh_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

def create_refresh_token(user_id: str, db: Session):
    raw = str(uuid.uuid4())
    hashed = hash_refresh_token(raw)

    db_token = RefreshToken(
        user_id=user_id,
        token_hash=hashed,
        expire=datetime.utcnow() + timedelta(days=REFRESH_TIME_DAY)
    )

    db.add(db_token)
    db.commit()

    return raw

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token,SECURITY_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")
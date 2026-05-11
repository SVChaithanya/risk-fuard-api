from schemas import UserCreate
from models import User
from auth import hash_password
from db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_user(data: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "successfully registered",
        "user_id": str(new_user.id)
    }
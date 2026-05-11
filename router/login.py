from models import User
from auth import verify_password, create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/login")
def login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id, db)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }
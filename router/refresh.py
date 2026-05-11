from schemas import RefreshTokenRequest
from fastapi import APIRouter, HTTPException, Depends
from db import get_db
from sqlalchemy.orm import Session
from models import RefreshToken
from datetime import datetime
from auth import create_access_token, create_refresh_token, hash_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):

    hashed = hash_refresh_token(data.refresh_token)

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == hashed
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if db_token.expire < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")

    user_id = db_token.user_id

    # 🔥 ROTATION
    db.delete(db_token)
    db.commit()

    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id, db)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }
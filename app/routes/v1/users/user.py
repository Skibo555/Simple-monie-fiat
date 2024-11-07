from app.schemas.schemas import UserRegisterForm, AuthResponse
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.oauth.oauth import get_current_user
from app.database.database import get_db
from app.utils.utils import hash
from app.models import models


router = APIRouter(
    prefix="/api/auth/user",
    tags=["User"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
async def register_user(user_data: UserRegisterForm, db: Session = Depends(get_db)):
    check_for_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if check_for_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"A user with {check_for_user.email} already exits.")
    username = db.query(models.User).filter(models.User.username == user_data.username).first()
    # if username.username == user_data.username:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail=f"That username {username.username} has been taken")
    user_password_hash = hash(user_data.password)
    user_data.password = user_password_hash

    new_user = models.User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

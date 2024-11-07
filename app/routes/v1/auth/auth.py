from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from starlette.background import BackgroundTasks
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.utils.utils import verify
from app.oauth.oauth import create_access_token, create_password_reset_token, decode_reset_password_token
from app.models.models import User
from app.schemas.schemas import ForgetPasswordRequest, ResetForgetPassword, SuccessMessageResetPassword
from app.service.email_server import send_mail
from app.config.config import settings
from app.utils.utils import hash























# This routers
router = APIRouter(
    prefix="/api/auth/user",
    tags=["Authentication"]
)


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    This endpoint is responsible for logging in an existing user.
    """
    user_email = user_data.username
    user_password = user_data.password
    # queries the database to get the user based on the details provided by the user.
    result = db.query(User).filter(User.email == user_email).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email address.")
    user_hashed_passwd = result.password
    verify_user_password = verify(user_password, user_hashed_passwd)

    if not verify_user_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password.")

    # This generates a jwt token for the user provided the user exists on the db, encodes the users' details
    # the details are the user's username, user_id and user_email.
    access_token = create_access_token(data={"user_id": result.id, "user_email": result.email, "username": result.username})

    return {
        "message": "You are successfully logged in.",
        "access_token": access_token,
        "status_code": status.HTTP_200_OK,
        "status": "success"
    }


@router.post("/forget-password")
async def forget_password(
        background_tasks: BackgroundTasks, passwd_reset_form: ForgetPasswordRequest, db: Session = Depends(get_db)
):
    user_email = passwd_reset_form.email
    try:
        result = db.query(User).filter(User.email == user_email).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email address")
        token = create_password_reset_token(email=result.email)
        url = f"{settings.BASE_URL}/api/auth/user/reset-password/{token}"
        message = (f"You requested for a password reset on out site, Simpl Monie, please find click on the link sent "
                   f"to you in this mail to reset your password. This link expires in 10 minutes.\n\n\n{url}")
        await send_mail(user_mail=[result.email], subject="Password Reset Link", body=message)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Email has been sent", "success": True,
                                     "status_code": status.HTTP_200_OK, "reset_link": url})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Something Unexpected, Server Error {str(e)}")


@router.get("/reset-password/{token}", response_model=SuccessMessageResetPassword)
async def reset_password(token: str, rfp: ResetForgetPassword, db: Session = Depends(get_db)):
    try:
        email: str = decode_reset_password_token(token=token)
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid Password Reset Payload or Reset Link Expired")
        if rfp.new_password != rfp.confirm_password:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="New password and confirm password are not same.")

        hashed_password = hash(rfp.new_password)
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        user.password = hashed_password
        db.add(user)
        db.commit()
        return {'success': True, 'status_code': status.HTTP_200_OK,
                'message': 'Password Reset Successful!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail=f"Some thing unexpected happened! {str(e)}")

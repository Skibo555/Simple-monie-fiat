import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config.config import settings
from app.schemas.schemas import TokenData


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
PASSWORD_RESET_EXPIRE_MINUTES = settings.PASSWORD_REST_EXPIRE_MINUTES
PASSWORD_RESET_SECRET_KEY = settings.RESET_PASSWORD_SECRET_KEY


def create_access_token(data: dict):
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        user_email = payload.get("user_email")
        username = payload.get("username")
        if user_id is None or user_email is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, user_email=user_email, username=username)
    except PyJWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials provided.",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)


def create_password_reset_token(email: str):
    data = {"email": email, "exp": datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES)}
    token = jwt.encode(data, PASSWORD_RESET_SECRET_KEY, ALGORITHM)
    return token


def decode_reset_password_token(token: str):
    try:
        payload = jwt.decode(token, PASSWORD_RESET_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        return email
    except PyJWTError:
        return None

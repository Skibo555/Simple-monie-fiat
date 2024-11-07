from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv("../../.env"))


class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_TYPE: str
    DATABASE_USER: str
    DATABASE_HOST: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PASSWORD_REST_EXPIRE_MINUTES: int
    BASE_URL: str
    SENDER_MAIL_PASSWORD: str
    RESET_PASSWORD_SECRET_KEY: str
    SENDER_EMAIL: str
    SENDER_MAIL_SERVER: str
    SENDER_USERNAME: str
    MAIL_PORT: int = 465
    MAIL_STARTTLS: str = False
    MAIL_SSL_TLS: str = True
    USE_CREDENTIALS: str = True
    VALIDATE_CERTS: str = True

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()

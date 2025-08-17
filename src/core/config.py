from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DB_URL: str
    TEST_DB_URL: str

    MODE: Literal["PROD", "TEST"] = "TEST"

    REDIS_URL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str

    APP_HOST: str

    REDIS_HOST: str
    REDIS_PORT: str

    POSTGRES_TEST_DB: str
    POSTGRES_TEST_USER: str
    POSTGRES_TEST_PASSWORD: str
    POSTGRES_TEST_PORT: int

    class Config:
        env_file = env_path
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()  # type: ignore

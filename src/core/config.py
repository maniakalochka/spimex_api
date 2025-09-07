from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DB_URL: str

    REDIS_URL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = env_path
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()  # type: ignore

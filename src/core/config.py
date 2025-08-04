from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    DB_URL: str


settings = Settings() # type: ignore

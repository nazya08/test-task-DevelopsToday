import os
import secrets
from typing import Optional, Any, Dict, List, Union, ClassVar

from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator, AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Test task for DevelopsToday"
    API_STR: str = "/api"

    SERVER_NAME: str = "tz_developstoday"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    LOG_LEVEL: str = "debug"
    RELOAD: bool = True
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(
            cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = (
        f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
    )
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URL", mode="before")
    def assemble_db_connection(
            cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    CAT_API_KEY: str = os.getenv("CAT_API_KEY")

    class Config:
        case_sensitive = True


settings = Settings()

# from pydantic_settings import BaseSettings, SettingsConfigDict


# class DatabaseSettings(BaseSettings):
#     POSTGRES_SERVER: str
#     POSTGRES_PORT: int
#     POSTGRES_DB: str
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str

#     model_config = SettingsConfigDict(
#         env_file="./.env", env_ignore_empty=True, extra="ignore"
#     )

#     def POSTGRES_URL(self):
#         return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# db_settings = DatabaseSettings()  # type: ignore

from dotenv import load_dotenv
import os

from pydantic_settings import BaseSettings

load_dotenv()

POSTGRES_URL = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_SERVER")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}"


JWT_SECRET = os.getenv("JWT_SECRET")

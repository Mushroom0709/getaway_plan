import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "mysql+aiomysql://root:password@localhost:3306/getaway_plan"
    jwt_secret: str = "dev-secret-change-in-production"
    access_password_hash: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

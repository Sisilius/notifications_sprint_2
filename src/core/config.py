from logging import config as logging_config
from pathlib import Path

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


BASE_DIR = Path(__file__).parent.parent.parent.absolute()


class Settings(BaseSettings):
    project_name: str = Field(..., env='PROJECT_NAME')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')
    
    rabbit_host: str = Field(..., env='RABBIT_HOST')
    rabbit_port: str = Field(..., env='RABBIT_PORT')
    rabbit_user: str = Field(..., env='RABBIT_USER')
    rabbit_pass: str = Field(..., env='RABBIT_PASS')
    
    postgres_host: str = Field(default="db", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    postgres_user: str = Field(default="user", env="POSTGRES_USER")
    postgres_password: str = Field(default="12345", env="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="test_db", env="POSTGRES_DB")

    def get_db_uri(self):
        driver = "postgresql+asyncpg"
        return "{driver}://{user}:{password}@{host}:{port}/{db}".format(
            driver=driver,
            user=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db
        )
    
    def get_amqp_uri(self):
        return "amqp://{user}:{password}@{host}:{port}/".format(
            user=self.rabbit_user,
            password=self.rabbit_pass,
            host=self.rabbit_host,
            port=self.rabbit_port
        )

    class Config:
        env_file = BASE_DIR/'.env'


settings = Settings()


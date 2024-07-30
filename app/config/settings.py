from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Enum


class StatusMode(str, Enum):
    TEST = "test"
    DEV = "dev"

class Settings(BaseSettings):
    mode: str = Field(default=StatusMode.DEV)
    
    # region Настройки БД
    postgres_user: str = Field(default='postgres')
    postgres_password: str = Field(default='postgres')
    postgres_host: str = Field(default='localhost')
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default='pusto')
    # endregion
    
    @property
    def postgres_uri(self):
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
    
    model_config = SettingsConfigDict(env_file='.env')
    
settings = Settings()
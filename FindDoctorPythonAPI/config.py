from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 6025
    DATABASE_NAME: str = "agendamento_db"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    
    # C# API
    CSHARP_API_URL: str = "http://localhost:5210"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    class Config:
        env_file = ".env"

settings = Settings()

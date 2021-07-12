from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    API_KEY: str = Field(..., env='CLIENT_SECRET')
    TOKEN: str = Field(..., env='DISCORD_TOKEN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
settings = Settings()
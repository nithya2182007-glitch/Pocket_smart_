from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-this-to-a-long-random-secret"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"
    mock_ai: bool = True
    frontend_origin: str = "http://127.0.0.1:8000"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

@lru_cache
def get_settings():
    return Settings()

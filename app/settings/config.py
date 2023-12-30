from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    db_url:str
    ranker_api_key:str
    model_config = SettingsConfigDict(env_file=".ENV",extra="allow")
@lru_cache()
def get_settings():
    return Settings()

""" print("config.py called") """

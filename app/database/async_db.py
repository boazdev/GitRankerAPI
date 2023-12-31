from functools import lru_cache
from databases import Database, DatabaseURL
from app.settings.config import get_settings

async_database_instance=None
async def startup():
    global async_database_instance  # Declare global use
    url = get_settings().db_url.replace("#", "%23")
    async_database_instance=Database(url)
    await async_database_instance.connect()

async def shutdown():
    await async_database_instance.disconnect()

@lru_cache()
def get_async_db_instance()->Database:
    return async_database_instance

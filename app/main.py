from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users_router
from app.settings.config import get_settings
from app.database import async_db
app = FastAPI()
#models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    await async_db.startup()

@app.on_event("shutdown")
async def shutdown():
    await async_db.get_async_db_instance().disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router.router)

@app.get('/health',status_code=200,response_model=str)
def health_check():
    return "GitRankerAPI is running"

settings_obj = get_settings()
print(f'settings url: {settings_obj.db_url}')

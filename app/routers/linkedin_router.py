from fastapi import APIRouter, Depends, HTTPException

from app.database.async_sqla_db import get_db
from app.models.user_metadata_model import UserMetaData
from app.routers.users_router import verify_api_key
from app.schemas.linkedin_update_request import LinkedinUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserMetaDataSchema, UserMetaDataSchemaWithLinkedinId

from app.service import users_service

router = APIRouter(prefix="/linkedin",
                   tags=["linkedin profiles"])


@router.patch("/user/{username}", status_code=201)
async def update_linkedin_profile_id(user_data: LinkedinUpdateRequest, username:str, db: AsyncSession = Depends(get_db)):
    if(not verify_api_key(user_data.api_key)):
        raise HTTPException(status_code=401,detail="incorrect API key")
    user: UserMetaData = await users_service.get_user_by_username(username=username, db=db)
    if(user==None):
        raise HTTPException(404,f"User {username} was not found in GitRanker database")
    user_schema =  UserMetaDataSchemaWithLinkedinId.model_validate(user)
    #user.linkedin_profiles_id = user_data.profile_id
    user_schema.linkedin_profiles_id = user_data.profile_id
    await users_service.update_user_linkedin(user=user_schema,db=db)
    return user_schema
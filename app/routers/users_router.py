import csv
import io
import traceback
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from app.database.async_sqla_db import get_db
from app.models.user_code_data_model import UserCodeData
from app.schemas.fps_query_schema import FPSQueryParams
from app.schemas.programming_langs_schema import ProgrammingLangs, UserLinesCode

from app.schemas.user_create_request import UserCreateRequest
from app.schemas.user_schema import UserMetaDataSchema
from app.service import users_code_service, users_service
from app.service.github_scanner_service import GithubScannerService
from app.service.users_metadata_async_service import get_user_ranks
from app.settings.config import get_settings
from app.utils.helpers import convert_dict_to_model

router = APIRouter(prefix="/users", tags=["users"])
from app.schemas.options_schema import OptionsIn
#from app.service import users_service

import anyio
import time

router = APIRouter(prefix="/users_metadata",
                   tags=["users metadata"])


@router.post("/users", status_code=201)
async def create_user(user_data: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    if(not verify_api_key(user_data.api_key)):
        raise HTTPException(status_code=401,detail="incorrect API key")
    try:
        #print(f'users meta data received from process repos: {user_data}')
        #print(f'users meta data model dump: {user_data.user_meta_data.model_dump()}')
        user = await users_service.get_user_by_username(username=user_data.user_meta_data.username,db=db)
        if user==None:
            user = await users_service.create_user(user = user_data.user_meta_data,db=db)
            print(f'user id: {user.id}')
            user_lines_code = user_data.lines_by_languages
            user_lines_code.users_metadata_id = user.id
            await users_code_service.create_user_code(user_code=user_lines_code, db=db)
            return user
        else:
            user_meta_updated = await users_service.update_user(user_id=user.id,user = user_data.user_meta_data,db=db)
            user_lines_code = user_data.lines_by_languages
            user_lines_code.users_metadata_id = user.id
            await users_code_service.update_user_code(user_code=user_lines_code, db=db)
            print("updated user")
            return "updated user"

    except Exception as e:
        print(f'exception in user router: {e}')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))  # Handle errors gracefully

@router.get("/username/{username}")
async def get_user_metadata(username:str,db: AsyncSession = Depends(get_db)):
    return await users_service.get_user_by_username(username=username,db=db)

@router.get("/fps")
async def get_fps_data(params: FPSQueryParams = Depends(), filter_by: Annotated[list[str], Query()] = ["lines_code>=500", "commits<1000",
                                                                                                       "java>=100","java_repositories>=20","followers=10"],
                        db: AsyncSession = Depends(get_db)):
    users_metadata_lst = await users_service.get_users_metadata_fps(fps_params=params, filter_by_lst = filter_by, db=db)
    return users_metadata_lst

@router.get("/ranks/{username}",response_model=dict, status_code=200)
async def get_user_metadata_ranks_by_username(username:str, db: AsyncSession = Depends(get_db)):
    return await users_service.get_user_ranks_by_username2(username=username, db=db)
    

def verify_api_key(api_key:str)->bool:
    if(api_key!=get_settings().ranker_api_key):
        return False
    else:
        return True




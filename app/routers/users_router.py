import csv
import io
import traceback
from fastapi import APIRouter, Depends,HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
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
from app.database.db import get_db

import anyio
import time

router = APIRouter(prefix="/users_metadata",
                   tags=["users metadata"])

""" @router.post("/users", status_code=201)
async def create_user(user_data: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    if(not verify_api_key(user_data.api_key)):
        raise HTTPException(status_code=401,detail="incorrect API key")
    try:
        #print(f'users meta data received from process repos: {user_data}')
        #print(f'users meta data model dump: {user_data.user_meta_data.model_dump()}')
        user = await users_service.create_user(user = user_data.user_meta_data,db=db)
        user_lines_code = user_data.lines_by_languages
        user_lines_code.users_metadata_id = user.id
        #print(f'users code data model dump: {user_lines_code.model_dump()}')
        await users_code_service.create_user_code(user_code=user_lines_code, db=db)
        return "Created"

    except Exception as e:
        print(f'exception in user router: {e}')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))  # Handle errors gracefully """
    
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
async def get_fps_data(params: FPSQueryParams = Depends(), db: AsyncSession = Depends(get_db)):
    print(f'params: {params}')
    users_metadata_lst = await users_service.get_users_metadata_fps(fps_params=params, db=db)
    results = []
    """ for user in users_metadata_lst:
        jason ={}
        jason["meta"] = UserMetaDataSchema.model_validate(user)
        jason["code"] = ProgrammingLangs.model_validate(user.users_code_data)
        results.append(jason) """
    return users_metadata_lst

@router.get("/users/{username}",response_model=dict, status_code=200)
async def get_user_metadata_ranks(username:str):
    print("get user ranks request")
    github_scanner_service  = GithubScannerService()
    token = await github_scanner_service.get_user_metadata_token(username=username)
    user_data = None
    while(user_data==None):
        user_data = await github_scanner_service.get_user_metadata_by_token(token=token)
    csv_string = user_data
    reader = csv.DictReader(io.StringIO(csv_string))
    user_meta_data = next(reader)

    user_meta_data = convert_dict_to_model(user_meta_data)

    user_ranks = await get_user_ranks(user_meta_data)
    return user_ranks






def verify_api_key(api_key:str)->bool:
    if(api_key!=get_settings().ranker_api_key):
        return False
    else:
        return True
""" @router.get("/", response_model=dict, status_code=200)
def get_db_github_users(skip: int = 0, limit: int = 100,db:Session=Depends(get_db)):
    usernames_lst : list[user_schema.User] = users_service.get_users(db, skip,limit)
    usernames_lst_serial = list(map(lambda x:{"id":x.id, "username":x.username},usernames_lst))
    return {"users":usernames_lst_serial, "number_db_users":users_service.get_num_users(db)}

@router.get("/username/{username}",response_model=user_schema.User, status_code=200)
def get_user_by_username(username:str, db: Session = Depends(get_db)):
    return users_service.get_user_by_username(db,username)
 """

""" @router.post("/",response_model= user_schema.User,status_code=201)
def create_user(username:user_schema.UserCreate, db: Session = Depends(get_db)):
    resp = users_service.create_user(db,username)
    if resp==None:
        raise HTTPException(400,"Username already exist")
    return resp
 """
""" @router.delete("/",response_model=str, status_code=200)
def delete_all_users(db:Session=Depends(get_db)):
    resp = users_service.delete_all(db)
    return resp """



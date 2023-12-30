import traceback
from fastapi import APIRouter, Depends,HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schemas.programming_langs_schema import ProgrammingLangs, UserLinesCode

from app.schemas.user_create_request import UserCreateRequest
from app.service import users_code_service, users_service
from app.settings.config import get_settings

router = APIRouter(prefix="/users", tags=["users"])
from app.schemas.options_schema import OptionsIn
#from app.service import users_service
from app.database.db import get_db

import anyio
import time

router = APIRouter(prefix="/users_metadata",
                   tags=["users metadata"])

@router.post("/users", status_code=201)
def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    if(not verify_api_key(user_data.api_key)):
        raise HTTPException(status_code=401,detail="incorrect API key")
    try:
        print(f'users meta data received from process repos: {user_data}')
        print(f'users meta data model dump: {user_data.user_meta_data.model_dump()}')
        user = users_service.create_user(user = user_data.user_meta_data,db=db)
        user_lines_code = user_data.lines_by_languages
        user_lines_code.users_metadata_id = user.id
        print(f'users code data model dump: {user_lines_code.model_dump()}')
        users_code_service.create_user_code(user_code=user_lines_code, db=db)
        return user

    except Exception as e:
        print(f'exception in user router: {e}')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))  # Handle errors gracefully
    
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



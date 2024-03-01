from functools import wraps
import time
from psycopg2 import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy import func,text,asc, update #select, join
from typing import Optional
from app.constants.sql_constants import SQL_QUERY_MAX_RETRY
from app.models.user_metadata_model import UserMetaData
from app.models.user_code_data_model import UserCodeData
from app.schemas import user_schema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.schemas.fps_query_schema import FPSQueryParams
""" def retry_on_operational_error(retries=10, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    print(f'OperationalError: {e}, retrying {i} time...')
                    time.sleep(delay)
            raise OperationalError(f"Failed after {retries} retries")
        return wrapper
    return decorator """

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Adjusted to use async/await
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserMetaData]:
    result = await db.execute(select(UserMetaData).offset(skip).limit(limit))
    return result.scalars().all()

async def get_users_by_id_greater_than(db: AsyncSession, id: int, skip: int = 0, limit: int = 100) -> list[UserMetaData]:
    query = select(UserMetaData).where(UserMetaData.id >= id).order_by(asc(UserMetaData.id)).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_user_by_username(db: AsyncSession, username: str) -> UserMetaData:
    result = await db.execute(select(UserMetaData).where(UserMetaData.username == username))
    return result.scalars().first()

# This decorator might need adjustment for async retry logic
async def create_user(db: AsyncSession, user: user_schema.UserMetaDataSchema) -> Optional[user_schema.UserMetaDataSchemaWithId]:
    db_user = UserMetaData(**user.model_dump())
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user: user_schema.UserMetaDataSchema, user_id:int): #fill this function
    db_user = user
    await db.execute(update(UserMetaData).where(UserMetaData.id == user_id).values(**user.model_dump()))
    return db_user

async def get_users_metadata_fps(fps_params: FPSQueryParams,db: AsyncSession)->list:
    result = await db.execute(
        select(UserMetaData).join(UserCodeData)
        .options(joinedload(UserMetaData.users_code_data))
        .limit(20)
        .offset(0)
    )
    data_rows = result.scalars().all()
    

    return_data = [row_to_dict(row) for row in data_rows]

    #print(data)
    return return_data

def row_to_dict(row):
    data_dict = {col.name: getattr(row, col.name) for col in row.__table__.columns}
    if hasattr(row, 'users_code_data') and row.users_code_data is not None:
        user_code_data = row.users_code_data
        for col in user_code_data.__table__.columns:
            data_dict[f"{col.name}"] = getattr(user_code_data, col.name)
    return data_dict
    #return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())
""" def get_users(db: Session, skip: int = 0, limit: int = 100)->list[UserMetaData]:
    return db.query(UserMetaData).offset(skip).limit(limit).all()

def get_users_by_id_greater_than(db: Session, id: int, skip: int = 0, limit: int = 100)-> list[UserMetaData]:
    query = db.query(UserMetaData).filter(UserMetaData.id >= id)
    query = query.order_by(asc(UserMetaData.id))
    query = query.limit(limit)
    users = query.all()
    return users

def get_user_by_username(db: Session, username: str) -> UserMetaData: 
    return db.query(UserMetaData).filter(UserMetaData.username == username).first()


def get_user_by_id(db: Session, id: str):
    return db.query(UserMetaData).filter(UserMetaData.id == id).first()

@retry_on_operational_error(retries=SQL_QUERY_MAX_RETRY, delay=1)
def create_user(db: Session, user: user_schema.UserMetaDataSchema) -> Optional[user_schema.UserMetaDataSchemaWithId]:
    try:
        db_user = db.query(UserMetaData).filter(UserMetaData.username == user.username).first()
        if db_user:
            # Update the existing user
            for key, value in user.model_dump().items():
                setattr(db_user, key, value)
        else:
            # Create a new user
            db_user = UserMetaData(**user.model_dump())
            db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f'sql exception: {e}')
        raise

    

def get_num_users(db:Session):
    try:
        row_count = db.query(func.count(UserMetaData.id)).scalar()
        return row_count
    except Exception as e:
        print(f"Error: {e}")
        return -1 """
    




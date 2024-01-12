from functools import wraps
import time
from psycopg2 import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy import func,text,asc #select, join
from typing import Optional
from app.constants.sql_constants import SQL_QUERY_MAX_RETRY
from app.models.user_metadata_model import UserMetaData
from app.schemas import user_schema
from sqlalchemy.exc import IntegrityError

def retry_on_operational_error(retries=10, delay=1):
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
    return decorator

def get_users(db: Session, skip: int = 0, limit: int = 100)->list[UserMetaData]:
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

    

def create_users_from_lst(db:Session, user_lst : list[str])->int:
    num_users_added=0
    for user_str in user_lst:
        try:
            db_user_data = {
                'username': user_str  
            }
            db_user = UserMetaData(**db_user_data)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            num_users_added+=1
        except IntegrityError as e: #duplicate username 
            db.rollback()
            print(f"error adding user , user already exists: {user_str}")
        except Exception as e:
            db.rollback()
            print(f"error adding user {user_str}: {e.__str__()}")
    return num_users_added

def get_num_users(db:Session):
    try:
        row_count = db.query(func.count(UserMetaData.id)).scalar()
        return row_count
    except Exception as e:
        print(f"Error: {e}")
        return -1
    
def delete_all(db:Session):
    try:
        db.query(UserMetaData).delete()
        reset_cmd = text("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
        db.execute(reset_cmd)
        db.commit()
        return "deleted"
    except Exception as e:
        print(f"delete error: {e.__str__()}")
        return None



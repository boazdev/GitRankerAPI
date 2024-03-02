from functools import wraps
import time
from fastapi import HTTPException
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
from app.utils.fps_utils import apply_operator, parse_filter_str
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

async def update_user_linkedin(db: AsyncSession, user: user_schema.UserMetaDataSchemaWithLinkedinId): #fill this function
    db_user = user
    await db.execute(update(UserMetaData).where(UserMetaData.id == user.id).values(**user.model_dump()))
    return db_user

async def get_users_metadata_fps(fps_params: FPSQueryParams, filter_by_lst: list[str], db: AsyncSession) -> dict:
    # Base query with joins (no filters, limits, or offsets applied yet)
    base_query = select(UserMetaData).join(UserCodeData).options(joinedload(UserMetaData.users_code_data))
    
    # Apply dynamic filtering
    for filter_str in filter_by_lst:
        field, op, value = parse_filter_str(filter_str)
        if field and op:
            # Determine the correct model based on the field's existence
            model = UserMetaData if hasattr(UserMetaData, field) else UserCodeData
            column = getattr(model, field)
            condition = apply_operator(column, op, value)
            if condition is not None:
                base_query = base_query.where(condition)

    # Sorting
    if fps_params.sort_field and fps_params.sort_direction:
        sort_model = UserMetaData if hasattr(UserMetaData, fps_params.sort_field) else UserCodeData
        sort_column = getattr(sort_model, fps_params.sort_field)
        if fps_params.sort_direction == "desc":
            sort_column = sort_column.desc()
        base_query = base_query.order_by(sort_column)

    # Pagination
    page_start = (fps_params.page_start - 1) * fps_params.page_size
    final_query = base_query.limit(fps_params.page_size).offset(page_start)

    # Execute the query to fetch paginated data
    result = await db.execute(final_query)
    data_rows = result.scalars().all()

    # Count total rows matching filters (without pagination)
    count_result = await db.execute(
        select(func.count()).select_from(base_query.subquery())
    )
    total_rows = count_result.scalar_one()

    # Calculate total pages
    total_pages = (total_rows + fps_params.page_size - 1) // fps_params.page_size

    # Prepare and return data
    results = {
        "pagination": {
            "page": fps_params.page_start,
            "total_pages": total_pages,
            "total_count": total_rows
        },
        "data": [row_to_dict(row) for row in data_rows]
    }

    return results


async def get_user_ranks_by_username2(username: str, db: AsyncSession):
    # Raw SQL query
    sql = text("""
    WITH user_data AS (
        SELECT
            um.*,
            ucd.*,
            -- Add other fields from UserCodeData as needed
            ucd.id AS users_code_data_id
        FROM users_metadata um
        JOIN users_code_data ucd ON um.id = ucd.users_metadata_id
        WHERE um.username = :username
    ), rank_data AS (
        SELECT
            COUNT(*) AS total_users_cnt,
            COUNT(*) FILTER (WHERE um.commits >= (SELECT commits FROM user_data)) AS commits_rank,
            COUNT(*) FILTER (WHERE um.stars >= (SELECT stars FROM user_data)) AS stars_rank,
            COUNT(*) FILTER (WHERE um.forks >= (SELECT forks FROM user_data)) AS forks_rank,
            COUNT(*) FILTER (WHERE um.lines_code >= (SELECT lines_code FROM user_data)) AS lines_code_rank,
            COUNT(*) FILTER (WHERE um.lines_tests >= (SELECT lines_tests FROM user_data)) AS lines_tests_rank,
            COUNT(*) FILTER (WHERE um.followers >= (SELECT followers FROM user_data)) AS followers_rank,
            COUNT(*) FILTER (WHERE um.followers >= (SELECT following FROM user_data)) AS following_rank,
            COUNT(*) FILTER (WHERE um.public_repos >= (SELECT public_repos FROM user_data)) AS public_repos_rank,
            COUNT(*) FILTER (WHERE um.public_repos >= (SELECT forked_repos FROM user_data)) AS forked_repos_rank,
            COUNT(*) FILTER (WHERE ucd.java >= (SELECT java FROM user_data)) AS java_rank,
            COUNT(*) FILTER (WHERE ucd.py >= (SELECT py FROM user_data)) AS py_rank,
            COUNT(*) FILTER (WHERE ucd.js >= (SELECT js FROM user_data)) AS js_rank,
            COUNT(*) FILTER (WHERE ucd.php >= (SELECT php FROM user_data)) AS php_rank,
            COUNT(*) FILTER (WHERE ucd.rb >= (SELECT rb FROM user_data)) AS rb_rank,
            COUNT(*) FILTER (WHERE ucd.cpp >= (SELECT cpp FROM user_data)) AS cpp_rank,
            COUNT(*) FILTER (WHERE ucd.h >= (SELECT h FROM user_data)) AS h_rank,
            COUNT(*) FILTER (WHERE ucd.c >= (SELECT c FROM user_data)) AS c_rank,
            COUNT(*) FILTER (WHERE ucd.cs >= (SELECT cs FROM user_data)) AS cs_rank,
            COUNT(*) FILTER (WHERE ucd.html >= (SELECT html FROM user_data)) AS html_rank,
            COUNT(*) FILTER (WHERE ucd.ipynb >= (SELECT ipynb FROM user_data)) AS ipynb_rank,
            COUNT(*) FILTER (WHERE ucd.css >= (SELECT css FROM user_data)) AS css_rank,
            COUNT(*) FILTER (WHERE ucd.ts >= (SELECT ts FROM user_data)) AS ts_rank,
            COUNT(*) FILTER (WHERE ucd.kt >= (SELECT kt FROM user_data)) AS kt_rank,
            COUNT(*) FILTER (WHERE ucd.dart >= (SELECT dart FROM user_data)) AS dart_rank,
            COUNT(*) FILTER (WHERE ucd.m >= (SELECT m FROM user_data)) AS m_rank,
            COUNT(*) FILTER (WHERE ucd.swift >= (SELECT swift FROM user_data)) AS swift_rank,
            COUNT(*) FILTER (WHERE ucd.go >= (SELECT go FROM user_data)) AS go_rank,
            COUNT(*) FILTER (WHERE ucd.rs >= (SELECT rs FROM user_data)) AS rs_rank,
            COUNT(*) FILTER (WHERE ucd.scala >= (SELECT scala FROM user_data)) AS scala_rank,
            COUNT(*) FILTER (WHERE ucd.scss >= (SELECT scss FROM user_data)) AS scss_rank,
            COUNT(*) FILTER (WHERE ucd.asm >= (SELECT asm FROM user_data)) AS asm_rank,
            COUNT(*) FILTER (WHERE ucd.pwn >= (SELECT pwn FROM user_data)) AS pwn_rank,
            COUNT(*) FILTER (WHERE ucd.inc >= (SELECT inc FROM user_data)) AS inc_rank

            -- Add other ranks from UserCodeData as needed
        FROM users_metadata um
        JOIN users_code_data ucd ON um.id = ucd.users_metadata_id
    )
    SELECT * FROM user_data, rank_data;
    """)

    result = await db.execute(sql, {"username": username})
    user_ranks = result.fetchone()

    if user_ranks:
        return dict(user_ranks)
    else:
        raise HTTPException(404,f"Github user {username} was not found in GitRanker database")

def row_to_dict(row):
    data_dict = {col.name: getattr(row, col.name) for col in row.__table__.columns}
    if hasattr(row, 'users_code_data') and row.users_code_data is not None:
        user_code_data = row.users_code_data
        for col in user_code_data.__table__.columns:
            data_dict[f"{col.name}"] = getattr(user_code_data, col.name)
    return data_dict
    #return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())

 
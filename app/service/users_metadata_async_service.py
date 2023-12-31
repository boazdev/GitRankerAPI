import json
from app.database.async_db import get_async_db_instance
from app.schemas.user_schema import UserMetaDataSchema
from databases.interfaces import Record
""" async def get_user_ranks(username:str,stars:str=0,commits:str=0,lines_code=0):
    database = get_async_db_instance()
    query = "SELECT * FROM users_metadata WHERE username = :username"
    result = await database.fetch_one(query=query, values={"username": "alonalj"})

    return result """

async def get_user_ranks(users_metadata: UserMetaDataSchema) -> dict:
    database = get_async_db_instance()
    query = """
        SELECT
            COUNT(*) AS users_cnt,
            COUNT(*) FILTER (WHERE commits >= :commits) AS commits,
            COUNT(*) FILTER (WHERE stars >= :stars) AS stars,
            COUNT(*) FILTER (WHERE forks >= :forks) AS forks,
            COUNT(*) FILTER (WHERE lines_code >= :lines_code) AS lines_code,
            COUNT(*) FILTER (WHERE lines_tests >= :lines_tests) AS lines_tests,
            COUNT(*) FILTER (WHERE followers >= :followers) AS followers,
            COUNT(*) FILTER (WHERE public_repos >= :public_repos) AS public_repos
        FROM users_metadata;
    """
    result: Record = await database.fetch_one(
        query=query,
        values={
            "commits": users_metadata.commits,
            "stars": users_metadata.stars,
            "forks": users_metadata.forks,
            "lines_code": users_metadata.lines_code,
            "lines_tests": users_metadata.lines_tests,
            "followers": users_metadata.followers,
            "public_repos": users_metadata.public_repos,
        }
    )
    ranks_data = {
        "users_total": result["users_cnt"],
        "commits": result["commits"],
        "stars": result["stars"],  # Adjust alias if needed
        "forks": result["forks"],
        "lines_code": result["lines_code"],
        "lines_tests": result["lines_tests"],
        "followers": result["followers"],
        "public_repos": result["public_repos"],
    }

    # Serialize as JSON:
    ranks_json = {"ranks": ranks_data, "username":users_metadata.username}

    return ranks_json  # TODO: Return a pydantic model with to_camel

    # Access and use the result data as needed
    #return result
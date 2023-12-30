from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema

class UserMetaDataSchema(BaseSchema):
    username: str = Field(..., alias="userName", unique=True)
    name: str 
    commits: int = Field(0, alias="commits")
    stars: int = Field(0, alias="stars")
    forks: int = Field(0, alias="forks")
    lines_code: int = Field(0, alias="linesCode")
    lines_tests: int = Field(0, alias="linesTests")
    followers: int = Field(0, alias="followers")
    following: int = Field(0, alias="following")
    public_repos: int = Field(0, alias="publicRepos")
    empty_repos: int = Field(0, alias="emptyRepos")
    forked_repos: int = Field(0, alias="forkedRepos")

class UserMetaDataSchemaWithId(BaseSchema):
    id: int

    
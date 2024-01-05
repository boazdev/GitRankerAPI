from ast import alias
from pydantic import BaseModel, Field,ConfigDict
from pydantic.alias_generators import to_snake
from app.schemas.base import BaseSchema

from app.schemas.programming_langs_schema import ProgrammingLangs, UserLinesCode

from app.schemas.user_schema import UserMetaDataSchema

class UserCreateRequest(BaseSchema):
    api_key:str = Field(...,alias="apiKey")
    user_meta_data: UserMetaDataSchema = Field(..., alias="userMetaData")
    lines_by_languages: UserLinesCode = Field(..., alias="linesByLanguages")


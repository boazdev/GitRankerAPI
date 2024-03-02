from pydantic import Field

from app.schemas.base import BaseSchema


class LinkedinUpdateRequest(BaseSchema):
    api_key:str = Field(...,alias="apiKey")
    profile_id: int = Field(...,alias="profileId")
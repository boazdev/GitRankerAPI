from pydantic import BaseModel, Field,ConfigDict
from pydantic.alias_generators import to_snake

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        
        populate_by_name=True,
        from_attributes=True,
        extra="forbid",

    )#alias_generator=to_snake,
from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel, Field

from enum import Enum

class FilterOperator(str, Enum):
    LT = "<"  # Less than
    GT = ">"  # Greater than
    GTE = ">="  # Greater than or equal to
    LTE = "<="  # Less than or equal to
    EQ = "="   # Equal to

class FPSQueryParams(BaseModel):
    sort_field: Optional[str] = Field(min_length=1,default="linesCode")
    sort_direction: Optional[str] = Field(pattern=r"^asc|desc$",default="desc")
    filter_field: Optional[str] = None
    filter_value: Optional[int] = None
    filter_operator: Optional[FilterOperator] = Field(default=FilterOperator.GTE)
    page_size: int = Query(10, ge=1)  # Default page size of 10
    page_start: int = Query(0, ge=0)
    filter_by: Optional[List[str]] = Query(None)
    sort_by: Optional[str] = Query(None)
    sort_direction: Optional[str] = Query(None)
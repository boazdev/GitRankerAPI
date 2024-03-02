from typing import Annotated, List, Optional
from fastapi import HTTPException, Query
from fastapi.datastructures import QueryParams
from pydantic import BaseModel, Field, validator
from typing import Literal

from enum import Enum

class FilterOperator(str, Enum):
    LT = "<"  # Less than
    GT = ">"  # Greater than
    GTE = ">="  # Greater than or equal to
    LTE = "<="  # Less than or equal to
    EQ = "="   # Equal to

class FPSQueryParams(BaseModel):
    #sort_field: Optional[str] = Field(min_length=1,default="lines_code",examples=["lines_code"])
    sort_field: Literal[
    'id',
    'username',
    'name',
    'commits',
    'stars',
    'forks',
    'lines_code',
    'lines_tests',
    'followers',
    'following',
    'public_repos',
    'empty_repos',
    'forked_repos',
    'created_at',
    'updated_at',
    "java",
    "py",
    "js",
    "php",
    "rb",
    "cpp",
    "h",
    "c",
    "cs",
    "html",
    "ipynb",
    "css",
    "ts",
    "kt",
    "dart",
    "m",
    "swift",
    "go",
    "rs",
    "scala",
    "scss",
    "asm",
    "pwn",
    "inc",
    "scss_repositories",
    "assembly_repositories",
    "pawn_repositories",
    "objectivec_repositories",
    "kotlin_repositories",
    "dart_repositories",
    "c_repositories",
    "typescript_repositories",
    "html_repositories",
    "java_repositories",
    "ejs_repositories",
    "csharp_repositories",
    "javascript_repositories",
    "jupyter_repositories",
    "cpp_repositories",
    "css_repositories",
    "python_repositories",
    "nodejs_repositories",
    "angular_repositories",
    "react_repositories",
    "dotnet_repositories",
    "php_repositories",
    "ruby_repositories",
    "scala_repositories",
    "swift_repositories",
    "go_repositories",
    "r_repositories",
    "rust_repositories"
]

    sort_direction : Literal['asc','desc']
    page_size: int = Query(10, ge=1)  # Default page size of 10
    page_start: int = Query(1, ge=1)

    @validator('page_size')
    def check_page_size(cls, v):
        if v > 100:
            raise HTTPException(422,'page_size must be 100 or less')
        return v

from typing import Optional

from pydantic import Field
from app.schemas.base import BaseSchema
class ProgLangsReposSchema(BaseSchema):
    scss_repositories: int = Field(default=0)
    assembly_repositories: int = Field(default=0)
    pawn_repositories: int = Field(default=0)
    objectivec_repositories: int = Field(default=0)  # Note: "objectivec" (no uppercase C)
    kotlin_repositories: int = Field(default=0)
    dart_repositories: int = Field(default=0)
    c_repositories: int = Field(default=0)
    typescript_repositories: int = Field(default=0)
    html_repositories: int = Field(default=0)
    java_repositories: int = Field(default=0)
    ejs_repositories: int = Field(default=0)
    csharp_repositories: int = Field(default=0)
    javascript_repositories: int = Field(default=0)
    jupyter_repositories: int = Field(default=0)
    cpp_repositories: int = Field(default=0)
    css_repositories: int = Field(default=0)
    python_repositories: int = Field(default=0)
    nodejs_repositories: int = Field(default=0)  # "nodejs" (no dot)
    angular_repositories: int = Field(default=0)
    react_repositories: int = Field(default=0)
    dotnet_repositories: int = Field(default=0)
    php_repositories: int = Field(default=0)
    ruby_repositories: int = Field(default=0)
    scala_repositories: int = Field(default=0)
    swift_repositories: int = Field(default=0)
    go_repositories: int = Field(default=0)
    r_repositories: int = Field(default=0)
    rust_repositories: int = Field(default=0)
    

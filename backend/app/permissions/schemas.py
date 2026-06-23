import re

from pydantic import BaseModel, ConfigDict, field_validator


class PermissionCreate(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.fullmatch(r"^\w+:\w+$", v):
            raise ValueError("name must follow the format 'resource:action'")
        return v


class PermissionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None and not re.fullmatch(r"^\w+:\w+$", v):
            raise ValueError("name must follow the format 'resource:action'")
        return v


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None

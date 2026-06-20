from pydantic import BaseModel, ConfigDict, model_validator


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    permissions: list[str]

    @model_validator(mode="before")
    @classmethod
    def extract_permission_names(cls, data: object) -> object:
        if hasattr(data, "permissions"):
            data.__dict__["permissions"] = [p.name for p in data.permissions]
        return data

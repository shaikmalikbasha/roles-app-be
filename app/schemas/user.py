from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool
    roles: list[str]

    @model_validator(mode="before")
    @classmethod
    def extract_role_names(cls, data: object) -> object:
        if hasattr(data, "roles"):
            data.__dict__["roles"] = [r.name for r in data.roles]
        return data

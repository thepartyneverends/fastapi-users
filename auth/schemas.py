from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    role_id: int

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: int

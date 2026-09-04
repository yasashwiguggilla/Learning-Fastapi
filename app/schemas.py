from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostUpdate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class VoteCreate(BaseModel):
    post_id: int
    dir: int
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class UserModel(BaseModel):
    id: int  # JSONPlaceholder user ID
    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str
    company: Company

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "extra": "ignore" 
    }

class UsersResponseModel(BaseModel):
    posts: List[UserModel]
    next_cursor: Optional[str] = None
    has_more: bool
    count: int
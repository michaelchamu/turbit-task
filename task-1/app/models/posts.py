from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, *args, **kwargs):
        from pydantic_core import core_schema
        return core_schema.str_schema()

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        return {"type": "string"}


class PostModel(BaseModel):
    id: int = Field(..., description="JSONPlaceholder post ID")
    userId: int = Field(..., description="ID of the user who created the post")
    title: str
    body: str

class PostsResponseModel(BaseModel):
    comments: List[PostModel]
    next_cursor: Optional[str] = None
    has_more: bool
    count: int
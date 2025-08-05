from pydantic import BaseModel, Field, EmailStr
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


class CommentModel(BaseModel):
    id: int = Field(..., description="JSONPlaceholder comment ID")
    postId: int = Field(..., description="ID of the related post")
    name: str
    email: EmailStr
    body: str

class CommentsResponseModel(BaseModel):
    comments: List[CommentModel]
    next_cursor: Optional[str] = None
    has_more: bool
    count: int
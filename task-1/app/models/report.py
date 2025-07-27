#model used to extract report data
#returns objects with the following fields:
#id: User ID
#name: User name
#username: User username
#posts: List of posts by the user
#comments: List of comments on the user's posts
#posts_count: Number of posts by the user
#comments_count: Number of comments on the user's posts

from pydantic import BaseModel, Field
from typing import List


class PostSummary(BaseModel):
    id: int
    title: str
    body: str


class CommentSummary(BaseModel):
    id: int
    postId: int
    name: str
    email: str
    body: str


class UserReportModel(BaseModel):
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="Full name of the user")
    username: str = Field(..., description="Username of the user")
    posts: List[PostSummary] = Field(default_factory=list, description="List of posts by the user")
    comments: List[CommentSummary] = Field(default_factory=list, description="List of comments on the user's posts")
    posts_count: int = Field(..., description="Number of posts by the user")
    comments_count: int = Field(..., description="Total number of comments on the user's posts")

from fastapi import APIRouter, HTTPException
from typing import List
from mongoconnector import mongo_connector
from ..models.posts import PostModel

route = APIRouter()

@route.get("/posts", response_model=List[PostModel])
async def get_posts():
    try:
        # Attempt to fetch posts from the database
        posts = await mongo_connector.mongodb.db['posts'].find().to_list(length=None)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
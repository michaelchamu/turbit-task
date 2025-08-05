from fastapi import APIRouter, HTTPException, Response, status
from typing import List
import logging
from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.posts import PostModel

route = APIRouter()
logger = logging.getLogger("task-1")

@route.get("/posts", response_model=List[PostModel])
async def get_posts():
    try:
        # Attempt to fetch posts from the database
        posts = await mongo_connector.mongodb.db['posts'].find().to_list(length=None)
        return posts or []
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@route.get("/posts/{post_id}", response_model=PostModel)
async def get_single_post(post_id: int):
    try:
        post = await mongo_connector.mongodb.db['posts'].find_one({"id": post_id})
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error") 

from fastapi import APIRouter, HTTPException, status
from typing import List

from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.posts import PostModel

route = APIRouter()

@route.get("/posts", response_model=List[PostModel])
async def get_posts():
    try:
        # Attempt to fetch posts from the database
        posts = await mongo_connector.mongodb.db['posts'].find().to_list(length=None)
        if not posts:
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content=[]
            )
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
from fastapi import APIRouter, HTTPException, Response, status
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
        if not posts:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@route.get("/posts/{post_id}", response_model=PostModel)
async def get_single_post(post_id: int):
    try:
        post = await mongo_connector.mongodb.db['posts'].find_one({"id": post_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error: " + str(e)) 

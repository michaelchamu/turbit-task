from fastapi import APIRouter, HTTPException, Response, status
from typing import List

from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.posts import PostModel

route = APIRouter()

@route.get("/posts",
           response_model=List[PostModel],
           description="Fetches full list of posts in collection",
           responses={
               status.HTTP_200_OK:{
                   "description": "All posts were fetched successfully"
               },
               status.HTTP_204_NO_CONTENT:{
                   "description": "Query ran successfully but there are no posts to show"
               },
               status.HTTP_500_INTERNAL_SERVER_ERROR:{
                   "description": "There was an error in the code, check exception body for details"
               }
               })
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
    
@route.get("/posts/{post_id}",
           response_model=PostModel,
           description="Fetches single post by ID in collection",
           responses={
               status.HTTP_200_OK:{
                   "description": "Single post retrieval successful"
               },
               status.HTTP_404_NOT_FOUND:{
                   "description": "Single post with id not found"
               },
               status.HTTP_500_INTERNAL_SERVER_ERROR:{
                   "description": "There was an error in the code, check exception body for details"
               }
               })
async def get_single_post(post_id: int):
    try:
        post = await mongo_connector.mongodb.db['posts'].find_one({"id": post_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error: " + str(e)) 

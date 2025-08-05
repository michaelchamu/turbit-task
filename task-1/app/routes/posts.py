from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List, Optional
import logging
from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.posts import PostModel, PostsResponseModel

route = APIRouter()
logger = logging.getLogger("task-1")

@route.get("/posts", response_model=PostsResponseModel)
async def get_posts(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    post_id: Optional[int] = Query(None)
    ):
    try:
        query_filter = {}

        if post_id is not None:
            query_filter["post_id"] = post_id
        
        if cursor:
            try:
                cursor_id = ObjectId(cursor)
                query_filter["_id"] = {"$lt": cursor_id}
            except Exception as ex:
                logger.error(str(ex))
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unexpected error")
            
        cursor_motor = mongo_connector.mongodb.db['posts'].find(query_filter)
        cursor_motor = cursor_motor.sort("_id", -1).limit(limit+1)

        posts_list = await cursor_motor.to_list(length=limit + 1)

        has_more = len(posts_list) > limit

        if has_more:
            posts_list = posts_list[:-1]

        next_cursor = None
        if has_more and posts_list:
            next_cursor = str(posts_list[-1]["_id"])

        result = PostsResponseModel(
            posts=posts_list,
            next_cursor=next_cursor,
            has_more=has_more,
            count=len(posts_list)
        )
        return result
    
    except Exception as ex:
        logger.error(str(ex))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")
    

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

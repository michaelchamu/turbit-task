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
    '''
    Fetches all posts from database.
    To cater for potential increases in number of documents, I use a cursor
    to fetch a limited number of records.
    Client side can then paginate to only access a small number of docs.
    I use the ObjectId of the last post from the previous batch.

    Args:
        cursor:
        limit: total number of posts to return
        post_id:
    Returns:
        PostsReturnModel: Object with a list of posts, id of next cursor etc.
    '''
    try:
        #setup the query filter to be used to fetch data
        query_filter = {}

        if post_id is not None:
            query_filter["post_id"] = post_id
        
        #configure the cursor to be used for the base pagination
        if cursor:
            try:
                #cursor must fit the ObjectID format of the MongoID so convert it here
                cursor_id = ObjectId(cursor)
                #fetch older documents/posts after the cursor
                query_filter["_id"] = {"$lt": cursor_id}

            except Exception as ex:
                logger.error(str(ex))
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unexpected error")

        #use motor's inbuilt feature for fetching documents 
        cursor_motor = mongo_connector.mongodb.db['posts'].find(query_filter)
        cursor_motor = cursor_motor.sort("_id", -1).limit(limit+1)

        posts_list = await cursor_motor.to_list(length=limit + 1)

        # confirm/check if there are more posts
        has_more = len(posts_list) > limit
        #if a there is a posts that goes above the limit, remove it here
        if has_more:
            posts_list = posts_list[:-1]
        # now get the next cursor which corresponds to the last post_id
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
        '''
        fetches single post by post id
        '''
        post = await mongo_connector.mongodb.db['posts'].find_one({"id": post_id})
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    except Exception:
        raise
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error") 

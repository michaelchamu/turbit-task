from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List, Optional

from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.comments import CommentModel, CommentsResponseModel
import logging

route = APIRouter()
logger = logging.getLogger("task-1")

@route.get("/comments", response_model=CommentsResponseModel)
async def get_comments(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    comment_id: Optional[int] = Query(
    None
    )):
    try:
        '''
        Fetches all comments from database.
        To cater for potential increases in number of documents, I use a cursor
        to fetch a limited number of records.
        Client side can then paginate to only access a small number of docs.
        I use the ObjectId of the last post from the previous batch.

        Args:
            cursor:
            limit: total number of posts to return
            comment_id:
        Returns:
            CommentsReturnModel: Object with a list of comments, id of next cursor etc.
        '''
        query_filter = {}

        if comment_id is not None:
            query_filter["comment_id"] = comment_id
        
        if cursor:
            try:
                cursor_id = ObjectId(cursor)
                query_filter["_id"] = {"$lt": cursor_id}
            except Exception as ex:
                logger.error(str(ex))
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unexpected error")
            
        cursor_motor = mongo_connector.mongodb.db['comments'].find(query_filter)
        cursor_motor = cursor_motor.sort("_id", -1).limit(limit+1)

        comments_list = await cursor_motor.to_list(length=limit + 1)

        has_more = len(comments_list) > limit

        if has_more:
            comments_list = comments_list[:-1]

        next_cursor = None
        if has_more and comments_list:
            next_cursor = str(comments_list[-1]["_id"])

        result = CommentsResponseModel(
            comments=comments_list,
            next_cursor=next_cursor,
            has_more=has_more,
            count=len(comments_list)
        )
        return result
    
    except Exception as ex:
        logger.error(str(ex))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")


@route.get("/comments/{comment_id}", response_model=CommentModel)
async def get_single_comment(comment_id: int):
    try:
        '''
        fetches single comment from the comments collection by comment_id
        uses the comment_id from json placeholder instead of the ObjectId from mongo
        '''
        comment = await mongo_connector.mongodb.db["comments"].find_one({"id": comment_id})
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return comment
    except Exception:
        raise
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error ") 


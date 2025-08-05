#all routes to access user data
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import Optional
import logging
from mongoconnector import mongo_connector
from ..models.user import UserModel, UsersResponseModel

route = APIRouter()
logger = logging.getLogger("task-2")

@route.get("/users", response_model=UsersResponseModel)
async def get_users(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    post_id: Optional[int] = Query(None)
    ):
    try:
        '''
        Fetches all users from database.
        To cater for potential increases in number of documents, I use a cursor
        to fetch a limited number of records.
        Client side can then paginate to only access a small number of docs.
        I use the ObjectId of the last post from the previous batch.

        Args:
            cursor:
            limit: total number of posts to return
            users_id:
        Returns:
            UsersReturnModel: Object with a list of users, id of next cursor etc.
        '''
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
            
        cursor_motor = mongo_connector.mongodb.db['users'].find(query_filter)
        cursor_motor = cursor_motor.sort("_id", -1).limit(limit+1)

        users_list = await cursor_motor.to_list(length=limit + 1)

        has_more = len(users_list) > limit

        if has_more:
            users_list = users_list[:-1]

        next_cursor = None
        if has_more and users_list:
            next_cursor = str(users_list[-1]["_id"])

        result = UsersResponseModel(
            users=users_list,
            next_cursor=next_cursor,
            has_more=has_more,
            count=len(users_list)
        )
        return result
    
    except Exception as ex:
        logger.error(str(ex))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")
     
@route.get("/users/{user_id}", response_model=UserModel)
async def get_single_user(user_id: int):
    try:
        user = await mongo_connector.mongodb.db['users'].find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return user
    except Exception as e:
         logger.error(str(e))
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error.") 


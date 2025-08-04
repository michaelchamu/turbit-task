#all routes to access user data
from fastapi import APIRouter, HTTPException, status
from typing import List

from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.user import UserModel

route = APIRouter()

@route.get("/users", response_model=List[UserModel])
async def get_users():
    try:
        # attempt fetch users from the data database
        users = await mongo_connector.mongodb.db['users'].find().to_list(length=None)
        if not users:
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content=[]
            )
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
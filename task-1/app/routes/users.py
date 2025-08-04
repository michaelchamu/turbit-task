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
    
@route.get("/users/{user_id}", response_model=UserModel)
async def get_single_user(user_id: int):
    try:
        user = await mongo_connector.mongodb.db['users'].find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Post not found")
        return user
    except Exception as e:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error: " + str(e)) 


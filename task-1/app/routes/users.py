#all routes to access user data
from fastapi import APIRouter, HTTPException
from typing import List
from ..database import mongo_connector
from ..models.user import UserModel

route = APIRouter()

@route.get("/users", response_model=List[UserModel])
async def get_users():
    try:
        # attempt fetch users from the data database
        users = await mongo_connector.mongodb.db['users'].find().to_list(length=None)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
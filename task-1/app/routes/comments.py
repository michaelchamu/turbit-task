from fastapi import APIRouter, HTTPException
from typing import List

from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.comments import CommentModel

route = APIRouter()

@route.get("/comments", response_model=List[CommentModel])
async def get_comments():
    try:
        # Attempt to fetch comments from the database
        comments = await mongo_connector.mongodb.db['comments'].find().to_list(length=None)
        if not comments:
            return JSONResponse(
                status_code=204,
                content=[]
            )
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
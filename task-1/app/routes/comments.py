from fastapi import APIRouter, HTTPException, status
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
                status_code=status.HTTP_204_NO_CONTENT,
                content=[]
            )
        return comments
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
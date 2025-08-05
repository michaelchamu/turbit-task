from fastapi import APIRouter, HTTPException, Query, status, Response
from typing import List
import logging
from fastapi.responses import JSONResponse
from mongoconnector import mongo_connector
from ..models.report import CommentSummary, PostSummary, UserReportModel

route = APIRouter()
logger = logging.getLogger("task-1")

@route.get("/reports", response_model=List[UserReportModel])
async def get_user_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    try:
        '''
        Fetches list of users, their posts and comments to their posts
        Instead of pulling all values frokm db into memory, it uses mongo pipelines
        for better memory management and also handles pagination by default
        '''
        skip = (page - 1) * limit

        #setup the aggregation pipeline here
        pipeline = [
            {"$skip": skip},
            {"$limit": limit},
            {
                "$lookup": {
                    "from": "posts",
                    "localField": "id",
                    "foreignField": "userId",
                    "as": "posts"
                }
            },
            {
                "$lookup": {
                    "from": "comments",
                    "localField": "posts.id",
                    "foreignField": "postId",
                    "as": "comments"
                }
            },
            {
                "$addFields": {
                    "posts_count": {"$size": "$posts"},
                    "comments_count": {"$size": "$comments"}
                }
            }
        ]

        # return users with their data
        users_data = await mongo_connector.mongodb.db['users'].aggregate(pipeline).to_list(length=None)

        if not users_data:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        reports = [
            UserReportModel(
                id=user['id'],
                name=user['name'],
                username=user['username'],
                posts=[PostSummary(**post) for post in user['posts']],
                comments=[CommentSummary(**comment) for comment in user['comments']],
                posts_count=user['posts_count'],
                comments_count=user['comments_count']
            )
            for user in users_data
        ]
        
        return reports
    except Exception as ex:
        logger.error(str(ex))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error.")
    
#this route fetches a report for a specific user by their ID
@route.get("/reports/{user_id}", response_model=UserReportModel)
async def get_user_report(user_id: int):
    try:
        # Fetch user, posts, and comments from the database
        user = await mongo_connector.mongodb.db['users'].find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        posts = await mongo_connector.mongodb.db['posts'].find({"userId": user_id}).to_list(length=None)
        comments = await mongo_connector.mongodb.db['comments'].find({"postId": {"$in": [post['id'] for post in posts]}}).to_list(length=None)
        # Process and compile user report
        report = UserReportModel(
            id=user['id'],
            name=user['name'],
            username=user['username'],
            posts=[PostSummary(**post) for post in posts],
            comments=[CommentSummary(**comment) for comment in comments],
            posts_count=len(posts),
            comments_count=len(comments)
        )
        #no need to check if report is empty because it will always have the user at the minimum
        return report
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error: " + str(e)) 
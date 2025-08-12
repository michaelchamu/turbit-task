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
    '''
        Fetches list of users, their posts and comments to their posts
        Instead of pulling all values frokm db into memory, it uses mongo pipelines and aggregation
        for better memory management and also handles pagination by default

        sending page and limit will cause pagination out the box
    '''
    try:
        skip = (page - 1) * limit

        #setup the aggregation pipeline here
        pipeline = [
            {"$skip": skip},
            {"$limit": limit},
            {
                #join User with their posts and store them in posts 'object'
                "$lookup": {
                    "from": "posts",
                    "localField": "id",
                    "foreignField": "userId",
                    "as": "posts"
                }
            },
            {
                #join user with the comments on their posts, store it as a comments 'object'
                "$lookup": {
                    "from": "comments",
                    "localField": "posts.id",
                    "foreignField": "postId",
                    "as": "comments"
                }
            },
            {
                #count the contents of the 2 objects in the 2 lookup queries
                "$addFields": {
                    "posts_count": {"$size": "$posts"},
                    "comments_count": {"$size": "$comments"}
                }
            }
        ]

        # return users with their data
        users_data = await mongo_connector.mongodb.db['users'].aggregate(pipeline).to_list(length=None)

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
    #catch any other exceptions and raise them again
    except Exception:
        raise
    except Exception as ex:
        logger.error(str(ex))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error.")
    
#this route fetches a report for a specific user by their ID
@route.get("/reports/{user_id}", response_model=UserReportModel)
async def get_user_report(user_id: int):
    '''
        Fetch single user report which includes their posts, and comments to the posts from the database. 
        uses a pipeline again which matches the user_id parameter
    '''
    try:
        #already check if user exists before we run the query
        user_exists = await mongo_connector.mongodb.db['users'].count_documents({"id": user_id}, limit=1)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        #setup the aggregation pipeline here
        pipeline = [
            {
                #match user ID here and then add the other pipeline valiues as before
                "$match": {
                    "id": user_id
                }
            },
            {
                #join User with their posts and store them in posts 'object'
                "$lookup": {
                    "from": "posts",
                    "localField": "id",
                    "foreignField": "userId",
                    "as": "posts"
                }
            },
            {
                #join user with the comments on their posts, store it as a comments 'object'
                "$lookup": {
                    "from": "comments",
                    "localField": "posts.id",
                    "foreignField": "postId",
                    "as": "comments"
                }
            },
            {
                #count the contents of the 2 objects in the 2 lookup queries
                "$addFields": {
                    "posts_count": {"$size": "$posts"},
                    "comments_count": {"$size": "$comments"}
                }
            }
        ]

        # return users with their data
        user_data = await mongo_connector.mongodb.db['users'].aggregate(pipeline).to_list(length=1)

        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        #return result as userreport model, doesnt include
        user = user_data[0]
        return UserReportModel(
            id=user['id'],
            name=user['name'],
            username=user['username'],
            posts=[PostSummary(**post) for post in user['posts']],
            comments=[CommentSummary(**comment) for comment in user['comments']],
            posts_count=user['posts_count'],
            comments_count=user['comments_count']
        )
    
    #to ensure that the 404 is returned to client correctly instead of a generic 500 raise the exception again
    except HTTPException:
        raise   
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error") 
from fastapi import APIRouter, HTTPException
from typing import List
from ..database import mongo_connector
from ..models.report import CommentSummary, PostSummary, UserReportModel

route = APIRouter()

@route.get("/reports", response_model=List[UserReportModel])
async def get_user_reports():
    try:
        # Fetch users, posts, and comments from the database
        users = await mongo_connector.mongodb.db['users'].find().to_list(length=None)
        posts = await mongo_connector.mongodb.db['posts'].find().to_list(length=None)
        comments = await mongo_connector.mongodb.db['comments'].find().to_list(length=None)

        # Process and compile user reports
        user_reports = []
        for user in users:
            user_posts = [post for post in posts if post['userId'] == user['id']]
            user_comments = [comment for comment in comments if comment['postId'] in [p['id'] for p in user_posts]]
            report = UserReportModel(
                id=user['id'],
                name=user['name'],
                username=user['username'],
                posts=[PostSummary(**post) for post in user_posts],
                comments=[CommentSummary(**comment) for comment in user_comments],
                posts_count=len(user_posts),
                comments_count=len(user_comments)
            )
            user_reports.append(report)

        return user_reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException

route = APIRouter()

@route.get("/users")
async def get_users():
    """
    Retrieve a list of users.
    """
    try:
        # Simulate fetching users from a database or service
        users = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Smith"}]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
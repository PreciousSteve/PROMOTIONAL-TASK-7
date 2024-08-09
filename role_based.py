# Role-Based Access Control API:

# Build an API that assigns roles to users (e.g., admin, user) and 
# restricts access to certain endpoints based on user roles.


from fastapi import FastAPI, Security, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    role: str


users_db = {
    1: {"id": 1, "username": "john", "role": "admin"},
    2: {"id": 2, "username": "jane", "role": "user"},
}


def get_current_user(user: User):
    if user.role != "user" or user.id != 2:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user

# Define the admin-only dependency
def get_admin_user(current_user: User):
    if current_user.role != "admin" or current_user.id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user

# Define a restricted endpoint for admins only
@app.get("/admin")
def read_admin_only(current_user:User = Depends(get_admin_user)):
    return {"message": f"Hello, admin {current_user.username}!"}

# Define a restricted endpoint for users only
@app.get("/user")
def read_user_only(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, user {current_user.username}!"}


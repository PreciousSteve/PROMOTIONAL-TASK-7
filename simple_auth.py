# Simple Authentication API:

# Build an API with basic authentication. Allow users to register and log in, and use hashed passwords for security. 
# Implement endpoints to protect certain resources that require authentication.
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


users_db = []


class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

security_detail = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/register")
def register(user: User):
    for u in users_db:
        if u.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
    hashed_password = get_password_hash(user.password)
    users_db.append(UserInDB(username=user.username, password=user.password, hashed_password=hashed_password))
    return {"username":user.username}

@app.post("/login")
def login(user:User):
    for user in users_db:
        if user.username == user.username and verify_password(user.password, user.hashed_password):
            return {"token_type": "bearer", "access_token": user.username}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )

@app.get("/users/me")
def read_users_me(token: str = Depends(security_detail)):
    for user in users_db:
        if user.username == token:
            return {"username":f"Welcome {user.username}"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

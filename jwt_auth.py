# JWT Authentication API:

# Develop an API that uses JSON Web Tokens (JWT) for user authentication. 
# Implement login and protected endpoints, ensuring only authenticated users can access certain resources.

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt

app = FastAPI()


SECRET_KEY = "205111"
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    password: str


security_detail = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/signup")
def sign(enter:User):
    return {"username":f"{enter.username}"}


@app.post("/login")
def login(user:User):
    data = {"user_identity": user.username}
    token = jwt.encode(data, SECRET_KEY)
    return {"token": token}


@app.get("/user")
def user(token=Depends(security_detail)):
    user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # user_id = user("user_id")
    return {"user info": user["user_identity"]}

    
        



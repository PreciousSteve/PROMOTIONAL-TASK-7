# API Key Authentication:

# Create an API that uses API keys for authentication. 
# Generate and validate API keys to restrict access to certain endpoints.

from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyQuery, APIKeyCookie, APIKeyHeader
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel

app = FastAPI()


class APIKey(BaseModel):
    key: str


api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


API_KEYS = {
    "1234567890": {"user_id": 1, "role": "admin"},
    "0987654321": {"user_id": 2, "role": "user"},
}

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
):
    api_key = api_key_query or api_key_header
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return API_KEYS[api_key]

# Defining a restricted endpoint
@app.get("/access")
def read_restricted(api_key = Depends(get_api_key)):
    return {"message": f"Hello, {api_key['role']}!"}

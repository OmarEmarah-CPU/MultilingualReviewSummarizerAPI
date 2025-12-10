import uuid
from fastapi import HTTPException, Header

# This dictionary acts as a simple in-memory database for registered clients
registered_clients = {}

def register_client():
    api_key = str(uuid.uuid4())
    registered_clients[api_key] = True
    return api_key

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key not in registered_clients:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
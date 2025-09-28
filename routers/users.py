from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_handler import create_token

login_user = APIRouter()

class User(BaseModel):
    username: str
    password: str

@login_user.post("/login", tags=["auth"])
def login(user: User):
    if user.username == "stiven" and user.password == "1234":
        token: str = create_token(user.model_dump())
        print(token)
        return JSONResponse(content={"token": token})
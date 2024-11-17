from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
import sys
from app.routers import task
from app.routers import user
# from routers import task
# from routers import user

import sys
sys.path.append("C:\\Users\\Alexey\\PycharmProjects\\modul_17_4_1")

app = FastAPI()
app.include_router(task.router)
app.include_router(user.router)

# @app.get("/")
# async def welcome(request: Request) -> HTMLResponse:
#     return {"message": "Welcome to Taskmanager"}

@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    return "<h1>Welcome to Taskmanager</h1>"

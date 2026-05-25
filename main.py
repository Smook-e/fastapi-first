from fastapi import FastAPI, status 
from pydantic import BaseModel
from app.routes.posts import router as posts_router
from app.routes.users import router as users_router
from app.routes.auth import router as auth_router
from database import create_tables
app = FastAPI()

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)
create_tables()
@app.get("/")
async def root():
    return {"message": "Hello World"}


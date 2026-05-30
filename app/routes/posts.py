from typing import Optional

from fastapi import APIRouter, HTTPException, status

from fastapi import FastAPI, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import create_tables, get_db
import models, schemas
from app.utils import oauth2





router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/" , response_model=list[schemas.PostOut])
async def get_posts(db : Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    return db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db : Session = Depends(get_db)):
    # db_post =  db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_posts(post: schemas.PostCreate, db : Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    db_post = models.Post(**post.model_dump())
    db_post.user_id = current_user.id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db : Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    db_post =  db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    db.delete(db_post)
    db.commit()
    return


@router.put("/{id}" , response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    db_post =  db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    for key, value in post.model_dump().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


from fastapi import APIRouter, HTTPException, status

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import create_tables, get_db
import models, schemas





router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/" , response_model=list[schemas.Post])
async def get_posts(db : Session = Depends(get_db)):
    return db.query(models.Post).all()

@router.get("/{id}" , response_model=schemas.Post)
async def get_post(id: int, db : Session = Depends(get_db)):
    db_post =  db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return db_post

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_posts(post: schemas.PostCreate, db : Session = Depends(get_db)):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db : Session = Depends(get_db)):
    db_post =  db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    db.delete(db_post)
    db.commit()
    return
@router.put("/{id}" , response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db)):
    db_post =  db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    for key, value in post.model_dump().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


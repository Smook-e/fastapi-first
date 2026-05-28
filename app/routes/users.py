from fastapi import APIRouter, Depends, HTTPException, status
from database import create_tables, get_db
from sqlalchemy.orm import Session
import models, schemas
from app.utils.hash import hash_password


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/" , response_model=list[schemas.User])
async def get_users(db : Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db : Session = Depends(get_db)):
    db_user =  db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return db_user

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    user.password = hash_password(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
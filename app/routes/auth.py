from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import schemas, models
from app.utils.hash import verify_password, dummy_hashed_password
from app.utils import oauth2

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
async def login(user_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.email == user_login.username).first()
    if not user:
        verify_password(user_login.password, dummy_hashed_password)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
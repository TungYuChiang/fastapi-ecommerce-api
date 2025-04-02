from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import UserCreate, UserLogin
from ..services.user import (
    create_user,
    authenticate_user,
    create_access_token,
)

router = APIRouter()


@router.post("/users/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return {"id": db_user.id, "username": db_user.username}


@router.post("/users/login")
def login_for_access_token(
    user_data: UserLogin, db: Session = Depends(get_db)
):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

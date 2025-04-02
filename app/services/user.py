from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..models.user import User
from ..schemas.user import UserCreate
from .jwt_service import JWTService
from ..database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

jwt_service = JWTService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    return jwt_service.create_access_token(data)


def decode_access_token(token: str):
    return jwt_service.decode_access_token(token)


def get_access_token_expire_minutes():
    return jwt_service.access_token_expire_minutes


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

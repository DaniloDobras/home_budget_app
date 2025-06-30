from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api.schema.auth_schema import RegisterRequest, LoginRequest
from app.utils.security import (
    verify_password, hash_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.db import models
from app.db.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(
        data: RegisterRequest,
        db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.username == data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    hashed_pw = hash_password(data.password)
    user = models.User(username=data.username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User registered successfully"}


@router.post("/token")
def login_for_access_token(
        form_data: LoginRequest,
        db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(
            models.User.username == form_data.username
        ).first()
    )
    if not user or not verify_password(
            form_data.password,
            user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "name": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

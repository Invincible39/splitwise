from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import user as user_schema
from app.services.user_service import UserService
from app.dependencies import get_db
from app.utils.auth import create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/sign_up", response_model=user_schema.User, summary="Register a new user")
def sign_up(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        new_user = UserService.create_user(db, user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=user_schema.Token, summary="User login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

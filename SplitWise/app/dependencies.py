# app/dependencies.py
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.utils.auth import verify_token
from app.models.user import User

def get_db(request: Request):
    """
    Dependency to get the DB session from the request.
    """
    return request.state.db

def get_current_user(token_data=Depends(verify_token), db: Session = Depends(get_db)):
    """
    Dependency to get the current authenticated user.
    """
    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

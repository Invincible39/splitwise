from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

class UserService:
    """
    Service for handling user-related operations.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = UserService.pwd_context.hash(user.password)
        db_user = User(name=user.name, email=user.email, password=hashed_password)
        db.add(db_user)
        db.flush()             
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = UserService.get_user_by_email(db, email)
        if not user or not UserService.pwd_context.verify(password, user.password):
            return False
        return user

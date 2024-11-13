from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    expenses_created = relationship('Expense', back_populates='creator')
    expense_splits = relationship('ExpenseSplit', back_populates='user')
    balances = relationship('Balance', back_populates='user')

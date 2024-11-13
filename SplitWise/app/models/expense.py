from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Expense(Base):
    """
    Represents an expense in the system.
    """
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    currency = Column(String)
    amount = Column(Float)
    expense_created_by = Column(Integer, ForeignKey('users.id'))
    split_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_settled = Column(Boolean, default=False)

    creator = relationship('User', back_populates='expenses_created')
    splits = relationship('ExpenseSplit', back_populates='expense')

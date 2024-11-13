from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ExpenseSplit(Base):
    """
    Represents the split of an expense among users.
    """
    __tablename__ = 'expense_splits'

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    amount_owed = Column(Float)
    is_settled = Column(Boolean, default=False)

    expense = relationship('Expense', back_populates='splits')
    user = relationship('User', back_populates='expense_splits')

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Balance(Base):
    """
    Represents the balance of a user in a specific currency.
    """
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    currency = Column(String)
    amount = Column(Float, default=0.0)

    user = relationship('User', back_populates='balances')

from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import List, Optional
from .enums import SplitTypeEnum

class ExpenseBase(BaseModel):
    description: str
    currency: str
    amount: float
    split_type: SplitTypeEnum

class ExpenseSplitBase(BaseModel):
    user_id: int
    amount_owed: Optional[float] = None

class ExpenseSplitCreate(ExpenseSplitBase):
    pass

class ExpenseCreate(ExpenseBase):
    splits: List[ExpenseSplitCreate]

    @model_validator(mode='after')
    def validate_splits(cls, values):
        split_type = values.split_type
        splits = values.splits
        if not splits:
            raise ValueError('Splits must be provided')

        if split_type == SplitTypeEnum.EQUAL:
            for split in splits:
                if split.amount_owed is not None:
                    raise ValueError('amount_owed should not be provided for equal splits')
        else:
            for split in splits:
                if split.amount_owed is None:
                    raise ValueError('amount_owed must be provided for percentage and unequal splits')
        return values

class ExpenseUpdate(ExpenseBase):
    splits: List[ExpenseSplitCreate]

    @model_validator(mode='after')
    def validate_splits(cls, values):
        return ExpenseCreate.validate_splits(values)

class Expense(ExpenseBase):
    id: int
    expense_created_by: int
    created_at: datetime
    is_settled: bool
    splits: List['ExpenseSplit']

    class Config:
        from_attributes = True

class ExpenseSplit(ExpenseSplitBase):
    id: int
    expense_id: int
    is_settled: bool

    class Config:
        from_attributes = True  

class Balance(BaseModel):
    id: int
    user_id: int
    currency: str
    amount: float

    class Config:
        from_attributes = True

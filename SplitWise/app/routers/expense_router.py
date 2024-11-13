from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import expense as expense_schema
from app.services.expense_service import ExpenseService
from app.dependencies import get_db, get_current_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/add_expense", response_model=expense_schema.Expense, summary="Add a new expense")
def add_expense(
    expense: expense_schema.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        new_expense = ExpenseService.create_expense(db, expense, current_user.id)
        return new_expense
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update_expense/{expense_id}", response_model=expense_schema.Expense, summary="Update an expense")
def update_expense(
    expense_id: int,
    expense: expense_schema.ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        updated_expense = ExpenseService.update_expense(db, expense_id, expense, current_user.id)
        return updated_expense
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_balance", response_model=List[expense_schema.Balance], summary="Get user balance")
def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    balances = ExpenseService.get_user_balance(db, current_user.id)
    return balances

@router.post("/settle_expense/{expense_id}", summary="Settle an expense")
def settle_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        ExpenseService.settle_expense(db, expense_id, current_user.id)
        return {"message": "Expense settled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list_expenses", response_model=List[expense_schema.Expense], summary="List user expenses")
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expenses = ExpenseService.get_user_expenses(db, current_user.id)
    return expenses

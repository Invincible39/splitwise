from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.user import User
from app.models.balance import Balance
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.utils.split_strategies import SplitStrategyFactory

class ExpenseService:
    """
    Service for handling expense-related operations.
    """

    @staticmethod
    def create_expense(db: Session, expense_data: ExpenseCreate, user_id: int):
        # Get the appropriate strategy for splitting the expense
        strategy = SplitStrategyFactory.get_strategy(expense_data.split_type)

        # Validate user IDs
        user_ids = [split.user_id for split in expense_data.splits]
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        if len(users) != len(user_ids):
            raise ValueError("One or more users not found")

        # Prepare split information
        splits_info = {split.user_id: split.amount_owed for split in expense_data.splits if split.amount_owed is not None}
        splits = strategy.calculate_splits(expense_data.amount, user_ids, splits_info)

        # Validate total split amount
        total_split_amount = sum(splits.values())
        if abs(total_split_amount - expense_data.amount) > 0.01:
            raise ValueError("Splits do not sum up to total amount")

        # Create expense
        expense = Expense(
            description=expense_data.description,
            currency=expense_data.currency,
            amount=expense_data.amount,
            expense_created_by=user_id,
            split_type=expense_data.split_type.value
        )
        db.add(expense)
        db.flush()
        db.refresh(expense)

        # Update balances and create splits
        for user_id, amount_owed in splits.items():
            expense_split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount_owed=amount_owed,
                is_settled=False
            )
            db.add(expense_split)

            # Update balances
            balance = db.query(Balance).filter(Balance.user_id == user_id, Balance.currency == expense_data.currency).first()
            if not balance:
                balance = Balance(user_id=user_id, currency=expense_data.currency, amount=0.0)
                db.add(balance)
            if user_id == expense.expense_created_by:
                # The creator of the expense
                balance.amount += expense_data.amount - amount_owed
            else:
                balance.amount -= amount_owed

        # No commit here; middleware will handle it
        return expense

    @staticmethod
    def update_expense(db: Session, expense_id: int, expense_data: ExpenseUpdate, user_id: int):
        # Fetch the expense
        expense = db.query(Expense).filter(Expense.id == expense_id, Expense.expense_created_by == user_id).first()
        if not expense:
            raise ValueError("Expense not found or not authorized")

        # Reverse previous balances
        old_splits = db.query(ExpenseSplit).filter(ExpenseSplit.expense_id == expense_id).all()
        for split in old_splits:
            balance = db.query(Balance).filter(Balance.user_id == split.user_id, Balance.currency == expense.currency).first()
            if split.user_id == expense.expense_created_by:
                balance.amount -= expense.amount - split.amount_owed
            else:
                balance.amount += split.amount_owed

        # Delete old splits
        db.query(ExpenseSplit).filter(ExpenseSplit.expense_id == expense_id).delete()
        db.flush()

        # Update expense
        expense.description = expense_data.description
        expense.currency = expense_data.currency
        expense.amount = expense_data.amount
        expense.split_type = expense_data.split_type.value
        expense.is_settled = False

        # Recalculate splits
        strategy = SplitStrategyFactory.get_strategy(expense_data.split_type)
        user_ids = [split.user_id for split in expense_data.splits]
        splits_info = {split.user_id: split.amount_owed for split in expense_data.splits if split.amount_owed is not None}
        splits = strategy.calculate_splits(expense_data.amount, user_ids, splits_info)

        # Validate total split amount
        total_split_amount = sum(splits.values())
        if abs(total_split_amount - expense_data.amount) > 0.01:
            raise ValueError("Splits do not sum up to total amount")

        # Create new splits and update balances
        for user_id, amount_owed in splits.items():
            expense_split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount_owed=amount_owed,
                is_settled=False
            )
            db.add(expense_split)

            # Update balances
            balance = db.query(Balance).filter(Balance.user_id == user_id, Balance.currency == expense.currency).first()
            if not balance:
                balance = Balance(user_id=user_id, currency=expense.currency, amount=0.0)
                db.add(balance)
            if user_id == expense.expense_created_by:
                balance.amount += expense.amount - amount_owed
            else:
                balance.amount -= amount_owed

        return expense

    @staticmethod
    def get_user_balance(db: Session, user_id: int):
        # Retrieve all balances for the user
        balances = db.query(Balance).filter(Balance.user_id == user_id).all()
        return balances

    @staticmethod
    def settle_expense(db: Session, expense_id: int, user_id: int):
        # Fetch the expense split
        split = db.query(ExpenseSplit).filter(ExpenseSplit.expense_id == expense_id, ExpenseSplit.user_id == user_id).first()
        if not split:
            raise ValueError("Expense split not found")
        if split.is_settled:
            raise ValueError("Expense already settled for this user")
        split.is_settled = True

        # Update balance
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        balance = db.query(Balance).filter(Balance.user_id == user_id, Balance.currency == expense.currency).first()
        balance.amount += split.amount_owed

        # Check if all splits are settled
        unsettled_splits = db.query(ExpenseSplit).filter(ExpenseSplit.expense_id == expense_id, ExpenseSplit.is_settled == False).count()
        if unsettled_splits == 0:
            expense.is_settled = True

        return split

    @staticmethod
    def get_user_expenses(db: Session, user_id: int):
        # Retrieve all expenses involving the user
        expenses = db.query(Expense).join(ExpenseSplit).filter(ExpenseSplit.user_id == user_id).all()
        return expenses

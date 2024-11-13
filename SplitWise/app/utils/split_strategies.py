from abc import ABC, abstractmethod
from typing import Dict, List
from app.schemas.enums import SplitTypeEnum

class SplitStrategy(ABC):
    """
    Abstract base class for split strategies.
    """
    @abstractmethod
    def calculate_splits(self, amount: float, users: list, splits_info: Dict[int, float] = None) -> Dict[int, float]:
        pass

class EqualSplitStrategy(SplitStrategy):
    """
    Strategy for equal splits.
    """
    def calculate_splits(self, amount: float, users: list, splits_info: Dict[int, float] = None) -> Dict[int, float]:
        per_person = amount / len(users)
        return {user_id: per_person for user_id in users}

class PercentageSplitStrategy(SplitStrategy):
    """
    Strategy for percentage splits.
    """
    def calculate_splits(self, amount: float, users: list, splits_info: Dict[int, float]) -> Dict[int, float]:
        total_percentage = sum(splits_info.values())
        if total_percentage != 100:
            raise ValueError("Total percentage must sum up to 100")
        return {user_id: amount * (percentage / 100) for user_id, percentage in splits_info.items()}

class UnequalSplitStrategy(SplitStrategy):
    """
    Strategy for unequal splits.
    """
    def calculate_splits(self, amount: float, users: list, splits_info: Dict[int, float]) -> Dict[int, float]:
        total_amount = sum(splits_info.values())
        if abs(total_amount - amount) > 0.01:
            raise ValueError("Total split amounts do not sum up to total amount")
        return splits_info

class SplitStrategyFactory:
    """
    Factory for creating split strategy instances.
    """
    @staticmethod
    def get_strategy(split_type: SplitTypeEnum) -> SplitStrategy:
        if split_type == SplitTypeEnum.EQUAL:
            return EqualSplitStrategy()
        elif split_type == SplitTypeEnum.PERCENTAGE:
            return PercentageSplitStrategy()
        elif split_type == SplitTypeEnum.UNEQUAL:
            return UnequalSplitStrategy()
        else:
            raise ValueError("Invalid split type")

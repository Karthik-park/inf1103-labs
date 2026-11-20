from __future__ import annotations
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        if percent <= 0 or percent > 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percent = percent

    def get_percent(self) -> float:
        return self.__percent

    def apply(self, total: float) -> float:
        return total * (1 - self.__percent / 100)
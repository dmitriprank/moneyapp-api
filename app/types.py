from enum import Enum


class TransactionType(Enum):
    DEPOSIT = 'deposit'
    EXPENSE = 'expense'

    def __repr__(self):
        return f"{self.value}"


class RecurrentFrequency(Enum):
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

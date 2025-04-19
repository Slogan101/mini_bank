from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from enum import Enum


class TransactionType(Enum):
    debit = "debit"
    credit = "credit"


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: Decimal


class DepositTransactionPayload(BaseModel):
    amount: Decimal

class Transaction(BaseModel):
    id: str
    account_id: str
    amount: Decimal
    transaction_type: str
    date: datetime

class DepositTransaction(BaseModel):
    account_id: str
    amount: Decimal
    transaction_type: str = TransactionType.credit.value
    date: datetime = datetime.now()


# class WithdrawTransaction(T)
class WithdrawTransaction(BaseModel):
    amount: Decimal
    transaction_type: str = TransactionType.debit.value
    date:datetime = datetime.now()

class WithdrawTransactionPayload(BaseModel):
    amount: Decimal


class TransactionDb(TransactionBase):
    account_id: str
    date: datetime

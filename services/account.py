from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from schemas.account import AccountCreatePayload, Account
from database import accounts_collection, transactions_collection
from schemas.transaction import DepositTransactionPayload, TransactionType, WithdrawTransactionPayload
from schemas.user import User
from serializers import account_serializer, transaction_seriliazer
from bson.objectid import ObjectId
from services.user import user_service


class AccountService:

    @staticmethod
    def create_account(account_data: AccountCreatePayload, user: User) -> Account:
        account_data = account_data.model_dump()
        account_with_defaults = Account(
            **account_data,
            user_id=user.id,
            balance=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        account_id = accounts_collection.insert_one(jsonable_encoder(account_with_defaults)).inserted_id
        account = accounts_collection.find_one({"_id": account_id})
        return account_serializer(account)


    @staticmethod
    def get_account(user: User):
        account = accounts_collection.find_one({"user_id": user.id})
        return account_serializer(account)
    

    @staticmethod
    def get_account_by_id(account_id: str):
        account = accounts_collection.find_one({"_id": ObjectId(account_id)})
        return account_serializer(account)

    @staticmethod
    def deposit_fund(deposit_payload: DepositTransactionPayload, account_id):
        account = AccountService.get_account_by_id(account_id)
        old_balance = float(account.balance)
        dep_amount = float(deposit_payload.amount)
        new_balance = old_balance + dep_amount
        account.balance = new_balance
        account = accounts_collection.find_one_and_update(
            {"_id": ObjectId(account.id)},
            {"$set": {"balance": new_balance, "updated_at": datetime.now()}}
        )
        transaction = AccountService.record_transaction(account_id, dep_amount, TransactionType.credit)
        return transaction_seriliazer(transaction)
        
    
    @staticmethod
    def withdraw_fund(current_user, withdraw_payload: str = WithdrawTransactionPayload):
        user = user_service.get_user_by_email(current_user.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        account = account_serializer(accounts_collection.find_one({"user_id": user.id}))
        print(account)
        old_balance = float(account.balance)
        withdraw_amount = float(withdraw_payload.amount)
        if old_balance < withdraw_amount:
            return {"message": "Insufficient Funds"}
        new_balance = old_balance - withdraw_amount
        account.balance = new_balance
        account_id = {"_id": ObjectId(account.id)}
        account_id = str(account_id["_id"])
        account = accounts_collection.find_one_and_update(
            {"_id": ObjectId(account.id)},
            {"$set": {"balance": new_balance, "updated_at": datetime.now()}}
        )
        transaction = AccountService.record_transaction(account_id, withdraw_amount, TransactionType.debit)
        return transaction_seriliazer(transaction)
    
    @staticmethod
    def record_transaction(
        account_id: str, amount: Decimal, transaction_type: TransactionType
    ):
        transaction = {
            "account_id": account_id,
            "amount": float(amount),
            "transaction_type": transaction_type.value,
            "date": datetime.now(),
        }
        result = transactions_collection.insert_one(transaction)
        return transactions_collection.find_one({"_id": result.inserted_id})


account_service = AccountService()

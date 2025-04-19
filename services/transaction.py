from database import transactions_collection, accounts_collection
from serializers import transaction_seriliazer, account_serializer
from services.user import user_service

class TransactionService:

    @staticmethod
    def get_transactions_for_account(current_user) -> list[dict]:
        user = user_service.get_user_by_email(current_user.email)
        if not user:
            raise 404
        account = account_serializer(accounts_collection.find_one({"user_id": user.id}))
        if not account:
            raise 404
        
        transaction_cursor = transactions_collection.find({"account_id": account.id}).sort("date", -1)
        return [transaction_seriliazer(txn) for txn in transaction_cursor]
    

transaction_service = TransactionService()
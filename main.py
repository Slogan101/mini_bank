from fastapi import FastAPI

from routes.user import user_router
from routes.account import account_router
from routes.transaction import transaction_router
from routes.account import limiter

app = FastAPI()

app.include_router(user_router, tags=["user"])
app.include_router(account_router, prefix="/accounts", tags=["account"])
app.include_router(transaction_router, prefix="/transaction", tags=['Transaction'])

app.state.limiter = limiter

@app.get('/')
def home():
    return {"message": "welcome to UserMoney"}

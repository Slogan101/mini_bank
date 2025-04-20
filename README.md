# 🏦 Mini Bank System Backend

This is a minimalistic banking backend built with **FastAPI** and **MongoDB**. It allows users to register, create accounts, deposit, withdraw funds,check their account balance securely, and view transaction history. Authentication is handled using **OAuth2** and **JWT**, and the withdrawal endpoint is protected by a **rate limiter** to control usage.

## 🚀 Features

- 🔐 User registration and login with OAuth2 & JWT
- 🧾 Account creation tied to user ID
- 💰 Deposit and withdraw funds
- 💳 View current balance
- 🛡️ Rate limiting (e.g. max 2 withdrawals per minute)
- 🧪 Validation using Pydantic

## 🛠️ Tech Stack

- FastAPI
- MongoDB (via PyMongo)
- Pydantic
- Python 3.12
- SlowAPI for rate limiting

## 🔧 Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/Slogan101/mini_bank
   cd user_money

2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Set your environment variables (JWT secret, DB URI, etc).

5. Run the application:
    uvicorn main:app --reload

📬 API Endpoints 
POST /register – Register a new user

POST /login – Get access token

GET /users - Get the authenticated user

GET /accounts - Get authenticated users account.

POST /accounts/create – Create an account

POST /accounts/deposit – Deposit funds

POST /accounts/withdraw – Withdraw funds

GET /transaction – View authenticated user transactions


📦 Future Improvements
OTP/email verification

Admin dashboard


📄 License
MIT License

Made with ❤️ by Slogan_codes
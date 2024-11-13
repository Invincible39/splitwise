# Split  Expenses

## Project Description

A simplified version of the expense-sharing application Splitwise. It allows users to:

- **Register** and **login** securely.
- **Add expenses** with different split types (equal, percentage, unequal).
- **Update expenses** they have created.
- **View their balance** with other users.
- **Settle expenses** with other users.
- **List all expenses** involving the user.

## Key Features

- **User Authentication**: Secure registration and login using hashed passwords and JWT tokens.
- **Expense Management**: Create, update, and settle expenses with various split strategies.
- **Split Strategies**: Implemented using the **Strategy Pattern** for equal, percentage, and unequal splits.
- **Balance Calculation**: Real-time calculation of user's total balance with others.
- **Design Principles**: Code adheres to **SOLID** principles and uses appropriate design patterns.
- **Middleware**: Custom middleware for processing time added.

## Technologies Used

- **FastAPI**: For building the API.
- **SQLAlchemy**: ORM for database interactions.
- **Supabase**: PostgreSQL database hosting.
- **Pydantic**: Data validation and settings management.
- **JWT**: Secure authentication.
- **Uvicorn**: ASGI server.

## How to Run the Application

- **Python 3.7+**
- **Virtual Environment**: Recommended to create a virtual environment.

### Steps


1. **Set Up Virtual Environment**

    python -m venv .venv
    source .venv/bin/activate  # On Windows use `venv\Scripts\activate`


2. **Install Dependencies**

    pip install -r requirements.txt

3. **Install Dependencies**

    Create a .env file in the root directory and add:
    DATABASE_URL=postgresql://username:password@host:port/database
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    Replace the DATABASE_URL with your Supabase PostgreSQL connection string.

4. **Table Creations**

    The application uses SQLAlchemy's Base.metadata.create_all to create tables. When you run the application for the first time, it will create all the necessary tables in the database.

5. **Starting Application**

    uvicorn app.main:app --reload


## For testing 

- **1. signup (name, email, password)**
- **2. If in swagger click on Authorize button and enter that email and password in username and password block and leave client columns empty**
- **3. You will get a token with which now you can test other apis**
- **4. Simply hit now other requests**
- **5. If in postman add that token in every request header as Authorization**
- **6.Happy Splittting!**

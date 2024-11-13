from fastapi import FastAPI
from app.routers import core_router,user_router, expense_router
from app.database import Base, engine
from app.middlewares import DBSessionMiddleware

app = FastAPI(
    title="Splitwise",
    description="An API for managing expenses, users, and balances in a Splitwise-like application.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Add middleware
app.add_middleware(DBSessionMiddleware)

# Include routers
app.include_router(core_router)
app.include_router(user_router)
app.include_router(expense_router)

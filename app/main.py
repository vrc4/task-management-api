from sqlalchemy import create_engine, inspect
from fastapi import FastAPI
from app.api import auth, task
from app.db.database import Base, engine
import app.models.user  # Ensure models are imported
import app.models.task

app = FastAPI(title="Task Management API")

# Create engine once (reuse it)
engine = create_engine("sqlite:///./test.db")

# Include routers
app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
def root():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return {"tables_in_db": tables}

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

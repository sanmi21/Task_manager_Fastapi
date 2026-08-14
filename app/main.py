from fastapi import FastAPI
from app.routers import auth, tasks
from app.database import engine
from app import models

# 1. Ensure database tables are created
# (We ran init_db.py yesterday, but this is a great safety net so the app never crashes on boot)
models.Base.metadata.create_all(bind=engine)

# 2. Initialize the FastAPI application
app = FastAPI(
    title="Task Manager API",
    description="A production-grade backend built with FastAPI and SQLite.",
    version="1.0.0"
)

# 3. Attach our Routers
app.include_router(auth.router)
app.include_router(tasks.router)

# 4. A simple health-check route to verify the server is running


@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API! Go to /docs to see the documentation."}

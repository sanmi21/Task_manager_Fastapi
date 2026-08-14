from app.database import Base, engine
from app.models import Task, User

print("Intializing the database....")

# Create all tables defined in Base subclasses (User and Task)
Base.metadata.create_all(bind=engine)

print("Database initialized successfully! 'tasks.db' has been created")

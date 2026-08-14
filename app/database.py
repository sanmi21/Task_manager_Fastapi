from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database URL string
# SQLite stores data in a simple file on disk named "tasks.db" inside your project root.
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# 2. Database Engine
# The engine manages the actual network/file connection to SQLite.
# connect_args={"check_same_thread": False} allows FastAPI's multi-threaded handlers
# to interact with the same SQLite connection safely.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Session Factory
# SessionLocal is a factory class that generates new database transaction sessions.
# autocommit=False ensures transactions aren't saved automatically without our consent.
# autoflush=False prevents automatic synchronization before queries are explicit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Declarative Base
# Base class that our ORM database models (User, Task) will inherit from.
Base = declarative_base()


# 5. DB Session Dependency
# This function creates a isolated database session for a single API request,
# yields it to the route, and closes it automatically when the request finishes.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
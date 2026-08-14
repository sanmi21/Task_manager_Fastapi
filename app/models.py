from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary key column (Auto-incrementing integer: 1, 2, 3...)
    id = Column(Integer, primary_key=True, index=True)

    # Unique constraint: No two users can register with the same email
    # Index: Speeds up searches when looking up users by email (O(log N) runtime)
    email = Column(String, unique=True, index=True, nullable=False)

    # Never store plain passwords! We will store hashed passwords here.
    hashed_password = Column(String, nullable=False)

    # Relationship to Task: One user can have many tasks
    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    # Foreign Key: References the 'id' column of the 'users' table
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to User: Every task belongs to one user
    owner = relationship("User", back_populates="tasks")
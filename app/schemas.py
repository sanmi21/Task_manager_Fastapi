from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# ----------------------------------
# USER SCHEMAS
# ----------------------------------

# 1. Used when a user registers (Incoming Request Body)
class UserCreate(BaseModel):
    email: EmailStr  # Automatically checks if string is a valid email format (e.g. user@domain.com)
    password: str    # Plain text password sent by user during registration


# 2. Used when returning user data in responses (Outgoing Response Body)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    # Pydantic V2 Syntax: Replaces the old 'class Config:'
    # This allows Pydantic to read data from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)


# ----------------------------------
# TOKEN SCHEMAS
# ----------------------------------

# Returned after a successful /login request
class Token(BaseModel):
    access_token: str
    token_type: str


# Embedded inside the JWT payload
class TokenData(BaseModel):
    user_id: Optional[int] = None


# ==========================================
# TASK SCHEMAS
# ==========================================

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
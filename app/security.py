from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import models
from app.database import get_db

# Load environment variables from .env file
load_dotenv()

# 1. Password Hashing Context using Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. JWT Configuration Constants
# IN PRODUCTION: Move SECRET_KEY to an environment variable (.env)
SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with a secure key in production
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ----------------------------------
# PASSWORD HASHING HELPERS
# ----------------------------------


def hash_password(password: str) -> str:
    """Takes a plain-text password and returns a secure bcrypt hash."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a typed plain-text password matches the stored bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------------
# JWT TOKEN HELPERS
# ----------------------------------


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a signed JSON Web Token (JWT) with an expiration timestamp."""
    to_encode = data.copy()

    # Set token expiration time (default 30 mins from now)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Add 'exp' claim to the token payload
    to_encode.update({"exp": expire})

    # Cryptographically sign the JWT using our SECRET_KEY and HS256 algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)

) -> models.User:
    """Extracts the current user from the JWT token in the Authorization header."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token to extract the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # Fetch the user from the database using the extracted user_id
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user

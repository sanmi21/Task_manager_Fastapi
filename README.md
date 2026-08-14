# Task Management REST API (FastAPI)

A high-performance, asynchronous RESTful API built with **Python**, **FastAPI**, **SQLAlchemy ORM**, **Pydantic v2**, and **SQLite**. Implements complete JWT authentication, `OAuth2PasswordBearer` integration, automated Swagger/OpenAPI documentation, and granular resource authorization.

---

## Tech Stack

- **Framework:** FastAPI
- **Database & ORM:** SQLite + SQLAlchemy
- **Data Validation & Serialization:** Pydantic (v2)
- **Security & Auth:** OAuth2 with Password Flow, JWT (`PyJWT`), `bcrypt` (Passlib)
- **API Documentation:** Interactive Swagger UI (`/docs`) & ReDoc (`/redoc`)

---

## Project Structure

task_api/
├── app/
│   ├── database.py       #SQLAlchemy engine & session dependency
│   ├── models.py         # SQLAlchemy DB models (User, Task)
│   ├── schemas.py        # Pydantic schemas
│   ├── security.py       # Password hashing & JWT generation
│   ├── routers/
│   │   ├── auth.py       # /auth/login and /auth/signup
│   │   └── tasks.py      # Protected Tasks CRUD endpoints
│   └── main.py           # FastAPI entrypoint & router inclusion
├── .env                  # Secrets (ignored by Git)
├── requirements.txt      # Python dependencies
└── README.md
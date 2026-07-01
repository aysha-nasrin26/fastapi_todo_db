# 🚀 FastAPI Task Management API

A secure Task Management REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL** featuring JWT Authentication and user-specific authorization.

---

## ✨ Features

- 🔐 User Registration
- 🔑 JWT Authentication
- 🔒 Protected Routes
- 👤 Current User Endpoint
- ✅ Create Task
- 📋 Get All Tasks
- 🔍 Search Tasks
- 📄 Pagination
- ↕️ Sorting
- 🎯 Status Filtering
- 📊 Task Statistics
- ✏️ Update Task
- 🗑 Delete Task
- 👥 User-specific Authorization

---

## 🛠 Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- JWT Authentication
- OAuth2
- Passlib (bcrypt)
- Pydantic

---

## 📁 Project Structure

```
fastapi_todo_db/
│
├── routers/
│   ├── auth.py
│   └── tasks.py
│
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/aysha-nasrin26/fastapi_todo_db.git

cd fastapi_todo_db

pip install -r requirements.txt
```

Create a `.env` file:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=your_database_url
```

Run the server:

```bash
uvicorn main:app --reload
```

---

## 📌 API Features

### Authentication

- Register
- Login
- Get Current User

### Tasks

- Create Task
- Get Tasks
- Get Task by ID
- Update Task
- Delete Task
- Search
- Pagination
- Sorting
- Status Filter
- Statistics

---

## 👩‍💻 Author

**Aysha Nasrin**

Aspiring Python Backend Developer

GitHub:
https://github.com/aysha-nasrin26

# MacV AI - Task Management System API

A lightweight **Task Management System API** built with **FastAPI**, **PostgreSQL**, **Celery**, and **Docker**.  
Includes JWT authentication, background workers, and email notifications.

---

## 🚀 Features
- **Projects**
  - Create, list, update, delete
  - View project details with all associated tasks
- **Tasks**
  - Create, list (filter, sort, paginate), update, delete
  - View task details with project + assigned user
- **Authentication**
  - JWT-based authentication
  - Access control (users only see their own data)
- **Email Notifications**
  - Task assignment & status change notifications
  - Daily overdue task summary
- **Background Jobs**
  - Celery workers with Redis
- **Deployment**
  - Dockerized app
  - GitHub Actions workflow for Docker image build

---

## 🗂 Tech Stack
- **Backend:** FastAPI
- **Database:** PostgreSQL (SQLAlchemy + Alembic)
- **Authentication:** JWT (PyJWT)
- **Background Jobs:** Celery + Redis
- **Email Service:** SMTP (configurable via `.env`)
- **Containerization:** Docker
- **CI/CD:** GitHub Actions

---

## 📦 Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/task-management-api.git
cd task-management-api

2️⃣ Environment Variables
Create a .env file in the root directory:

DATABASE_URL=postgresql+psycopg2://user:password@db:5432/task_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-email-password
REDIS_URL=redis://redis:6379/0

3️⃣ Run Locally with Docker

docker-compose up --build
This will start:

FastAPI app on http://localhost:8000

PostgreSQL

Redis

Celery worker

4️⃣ API Docs
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

5️⃣ Run Tests

pytest
🐳 Build & Push Docker Image (GitHub Actions)
This project is configured to automatically build & push a Docker image on every push to the main branch via GitHub Actions.

Create a repository on GitHub.

Add GitHub Secrets:

DOCKER_USERNAME → your Docker Hub username

DOCKER_PASSWORD → your Docker Hub password or access token

Push to the main branch — the workflow will:

Build Docker image

Push to Docker Hub as dockerhub-username/task-management-api:latest

🗄 Database Schema Diagram

User
----
id (PK)
username
email
password_hash

Project
-------
id (PK)
name
description
owner_id (FK → User.id)

Task
----
id (PK)
title
description
status
priority
due_date
project_id (FK → Project.id)
assigned_user_id (FK → User.id)

🔑 Authentication
Register: POST /auth/register

Login: POST /auth/login

Copy access_token from the login response.

Use as Bearer token in all authenticated requests.

📨 Email & Celery Setup
Emails are sent asynchronously via Celery workers.

Redis is used as the Celery broker.

Daily overdue task summary is scheduled via Celery Beat.

🛠 Deployment
Ensure .env is configured for production.

GitHub Actions will handle image build & push.

Deploy to any container hosting (e.g., Render, AWS ECS, Azure Container Apps, etc.).

📬 Contact
For questions, email krithik@macv.ai.
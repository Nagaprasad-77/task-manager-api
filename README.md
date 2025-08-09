# MacV AI - Task Management System API

A lightweight **Task Management System API** built with **FastAPI**, **PostgreSQL**, **Celery**, and **Docker**.  
Includes JWT authentication, background workers, and email notifications.  
**Live API:** [https://task-manager-api-gnnh.onrender.com](https://task-manager-api-gnnh.onrender.com)

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
  - GitHub Actions workflow for Docker image build & push

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

env

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

FastAPI app → http://localhost:8000

PostgreSQL

Redis

Celery worker

4️⃣ API Docs
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

5️⃣ Run Tests

pytest

🐳 Deployment
This project uses GitHub Actions to automatically:

Build Docker image

Push to Docker Hub: dockerhub-username/task-management-api:latest

Steps:

Create a GitHub repository.

Add GitHub Secrets:

DOCKER_USERNAME

DOCKER_PASSWORD

Push to main branch — workflow will run automatically.

Deploy container to Render/AWS/Azure.

🗄 Database Schema Diagram
mermaid
Copy
Edit
erDiagram
    User {
        int id PK
        string username
        string email
        string password_hash
    }
    Project {
        int id PK
        string name
        string description
        int owner_id FK
    }
    Task {
        int id PK
        string title
        string description
        string status
        string priority
        date due_date
        int project_id FK
        int assigned_user_id FK
    }
    User ||--o{ Project : owns
    User ||--o{ Task : assigned
    Project ||--o{ Task : contains

🔑 Authentication Flow
Register → POST /auth/register

Login → POST /auth/login

Copy access_token from login response.

Use token in Authorization header:

makefile

Authorization: Bearer <your_token>

📬 Email & Celery
Emails are sent asynchronously using Celery workers.

Redis acts as the message broker.

Celery Beat schedules daily overdue task summary.

📌 Useful Links
Live API: https://task-manager-api-gnnh.onrender.com

Swagger Docs: https://task-manager-api-gnnh.onrender.com/docs

📬 Contact
For any queries, reach out to krithik@macv.ai
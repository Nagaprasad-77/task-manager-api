from celery import Celery

# Local Redis connection (DB 0)
celery_app = Celery(
    "task_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Task routing
celery_app.conf.task_routes = {
    "app.tasks.email.send_email_task": {"queue": "email"}
}

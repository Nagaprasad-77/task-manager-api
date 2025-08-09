from app.tasks import celery_app

# Only export the Celery app — no worker_main()
__all__ = ("celery_app",)

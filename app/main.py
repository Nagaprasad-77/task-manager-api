# app/main.py
from fastapi import FastAPI
from app.routers import users, projects, tasks, notifications  # ✅ include notifications

app = FastAPI()

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(notifications.router)  # ✅ Add notifications route

@app.get("/")
def root():
    return {"message": "Welcome to Task Manager API!"}

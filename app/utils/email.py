def send_task_assigned_email(db, task):
    print(f"[Email Stub] Task '{task.title}' assigned to user ID {task.assigned_user_id}")

def send_task_update_email(db, task):
    print(f"[Email Stub] Task '{task.title}' updated. New status: {task.status}")

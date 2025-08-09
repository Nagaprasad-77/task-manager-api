from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, EmailStr
from app.tasks.email import send_email_task

router = APIRouter()

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    message: str

@router.post("/notify/send", status_code=status.HTTP_202_ACCEPTED)
def trigger_email(email: EmailRequest):
    try:
        send_email_task.delay(email.to_email, email.subject, email.message)
        return {"message": f"Email task triggered to {email.to_email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to queue email: {str(e)}")

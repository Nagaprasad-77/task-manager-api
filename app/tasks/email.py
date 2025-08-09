from app.tasks import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

@celery_app.task(name="app.tasks.email.send_email_task")
def send_email_task(to_email: str, subject: str, message: str):
    try:
        # ✅ Validate the email
        validate_email(to_email)

        # ✅ Get sender details from environment variables
        sender_email = os.getenv("EMAIL_HOST_USER")
        sender_password = os.getenv("EMAIL_HOST_PASSWORD")

        if not sender_email or not sender_password:
            raise ValueError("Email credentials are not set in .env")

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
        return f"Email sent to {to_email}"

    except EmailNotValidError as e:
        error_msg = f"Invalid email: {e}"
        print(f"❌ {error_msg}")
        return error_msg

    except Exception as e:
        error_msg = f"Failed to send email: {e}"
        print(f"❌ {error_msg}")
        return error_msg

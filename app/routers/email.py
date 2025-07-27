from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from app.dependencies import get_current_user
from app.models.user import User
from app.services.email_service import send_email
from app.services.log_service import log_activity

router = APIRouter()


class EmailSchema(BaseModel):
    to_email: EmailStr
    subject: str
    message: str


@router.post("/send-email")
def send_email_endpoint(
    email: EmailSchema, current_user: User = Depends(get_current_user)
):
    try:
        send_email(email.to_email, email.subject, email.message)
        log_activity(
            f"Email sent to {email.to_email} by user {current_user.email}"
        )
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

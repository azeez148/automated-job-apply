from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from app.dependencies import get_current_user
from app.models.user import User
from app.services.email_finder_service import find_emails
from app.services.log_service import log_activity

router = APIRouter()


class EmailFinderRequest(BaseModel):
    url: HttpUrl


@router.post("/find-emails")
def find_emails_endpoint(
    request: EmailFinderRequest, current_user: User = Depends(get_current_user)
):
    try:
        emails = find_emails(str(request.url))
        log_activity(
            f"Found emails on {request.url} by user {current_user.email}"
        )
        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

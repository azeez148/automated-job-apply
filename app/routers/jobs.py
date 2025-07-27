from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, HttpUrl

from app.dependencies import get_current_user
from app.models.user import User
from app.services.email_finder_service import find_emails
from app.services.email_service import send_email
from app.services.job_filter_service import filter_jobs
from app.services.log_service import log_activity
from app.services.scraper_service import scrape_jobs

router = APIRouter()


class JobRequest(BaseModel):
    company_url: HttpUrl
    job_keywords: List[str]
    email_subject: str
    email_message: str


@router.post("/find-and-apply")
def find_and_apply(
    request: JobRequest, current_user: User = Depends(get_current_user)
):
    try:
        # 1. Scrape the company's website
        links = scrape_jobs(str(request.company_url))
        log_activity(
            f"Scraped {request.company_url} for jobs by user {current_user.email}"
        )

        # 2. Filter for relevant jobs
        filtered_jobs = filter_jobs(links, request.job_keywords)
        log_activity(
            f"Filtered jobs for keywords {request.job_keywords} by user {current_user.email}"
        )

        if not filtered_jobs:
            return {"message": "No relevant jobs found."}

        # 3. Find the career email address
        emails = find_emails(str(request.company_url))
        log_activity(
            f"Found emails on {request.company_url} by user {current_user.email}"
        )

        if not emails:
            return {"message": "No career email address found."}

        # 4. Send an email to the first found email address
        to_email = emails[0]
        job_list = "\n".join(filtered_jobs)
        message = f"{request.email_message}\n\nHere are the jobs I'm interested in:\n{job_list}"
        send_email(to_email, request.email_subject, message)
        log_activity(
            f"Sent job application email to {to_email} by user {current_user.email}"
        )

        return {
            "message": f"Email sent to {to_email} with {len(filtered_jobs)} job links."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

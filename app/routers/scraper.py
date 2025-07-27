from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from app.dependencies import get_current_user
from app.models.user import User
from app.services.job_filter_service import filter_jobs
from app.services.log_service import log_activity
from app.services.scraper_service import scrape_jobs

router = APIRouter()


class ScrapeRequest(BaseModel):
    url: HttpUrl
    keywords: List[str]


@router.post("/scrape")
def scrape_url(
    request: ScrapeRequest, current_user: User = Depends(get_current_user)
):
    try:
        links = scrape_jobs(str(request.url))
        filtered_links = filter_jobs(links, request.keywords)
        log_activity(
            f"Scraped {request.url} for keywords {request.keywords} by user {current_user.email}"
        )
        return {"links": filtered_links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

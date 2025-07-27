from fastapi import Depends, FastAPI
from mangum import Mangum

from app.dependencies import get_current_user
from app.models.user import User
from app.routers import auth, email, scraper, email_finder, jobs

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(email.router, prefix="/email", tags=["email"])
app.include_router(scraper.router, prefix="/scraper", tags=["scraper"])
app.include_router(email_finder.router, prefix="/email-finder", tags=["email-finder"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


handler = Mangum(app)

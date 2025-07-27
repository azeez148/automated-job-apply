from pydantic import BaseSettings

class EmailSettings(BaseSettings):
    MAIL_USERNAME: str = "your-email@example.com"
    MAIL_PASSWORD: str = "your-password"
    MAIL_FROM: str = "your-email@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.example.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    class Config:
        case_sensitive = True

email_settings = EmailSettings()

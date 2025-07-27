import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.email_config import email_settings


def send_email(to_email: str, subject: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = email_settings.MAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(email_settings.MAIL_SERVER, email_settings.MAIL_PORT)
        server.set_debuglevel(1)
        server.starttls()
        server.login(email_settings.MAIL_USERNAME, email_settings.MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

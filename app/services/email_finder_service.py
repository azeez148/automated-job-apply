import re
import requests
from bs4 import BeautifulSoup


def find_emails(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        return list(set(emails))  # Return unique emails
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}")
        return []

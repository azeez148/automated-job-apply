import requests
from bs4 import BeautifulSoup


def scrape_jobs(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True)]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}")
        return []

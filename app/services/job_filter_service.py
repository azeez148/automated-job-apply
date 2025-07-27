from typing import List


def filter_jobs(job_links: List[str], keywords: List[str]) -> List[str]:
    filtered_jobs = []
    for link in job_links:
        for keyword in keywords:
            if keyword.lower() in link.lower():
                filtered_jobs.append(link)
                break
    return filtered_jobs

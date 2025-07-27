import csv
from datetime import datetime


def log_activity(activity: str):
    with open("activity_log.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now(), activity])

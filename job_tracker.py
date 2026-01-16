import requests
from bs4 import BeautifulSoup
import os

# ---------------- CONFIG ----------------

SEARCH_URL = (
    "https://www.naukri.com/accounts-executive-jobs-in-mumbai-navi-mumbai-pune"
    "?experience=3&salary=550000to700000"
)

SEEN_FILE = "jobs_seen.txt"

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

# ---------------------------------------


def load_seen_jobs():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()


def save_seen_jobs(job_ids):
    with open(SEEN_FILE, "w") as f:
        for jid in job_ids:
            f.write(jid + "\n")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload, timeout=30)


def main():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(SEARCH_URL, headers=headers, timeout=30)
    soup = BeautifulSoup(res.text, "html.parser")

    seen_jobs = load_seen_jobs()
    current_jobs = set()
    messages = []

    for job in soup.select("article.jobTuple"):
        job_id = job.get("data-job-id")
        if not job_id:
            continue

        current_jobs.add(job_id)

        if job_id not in seen_jobs:
            title = job.select_one("a.title").text.strip()
            company = job.select_one("a.subTitle").text.strip()
            location = job.select_one("li.location span").text.strip()
            link = job.select_one("a.title")["href"]

            msg = (
                f"🔔 <b>{title}</b>\n"
                f"{company}\n"
                f"{location}\n"
                f"<a href='{link}'>Apply here</a>"
            )
            messages.append(msg)

    if messages:
        final_msg = "📢 <b>New Naukri Job Alert</b>\n\n" + "\n\n".join(messages)
        send_telegram(final_msg)

    save_seen_jobs(current_jobs)


if __name__ == "__main__":
    main()

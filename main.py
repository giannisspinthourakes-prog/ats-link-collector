import requests
from bs4 import BeautifulSoup
import csv
import time

ATS_PATTERNS = [
    "jobs.lever.co",
    "job-boards.greenhouse.io",
    "jobs.ashbyhq.com",
    "careers.workday.com"
]

SEED_URLS = [
    "https://jobs.lever.co/appen",
    "https://job-boards.greenhouse.io/pagerduty",
    "https://jobs.ashbyhq.com/openai"
]

def extract_ats_links(url):
    links = set()
    try:
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if resp.status_code != 200:
            return links

        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            for pattern in ATS_PATTERNS:
                if pattern in href:
                    links.add(href.split("?")[0])
    except Exception as e:
        print(f"Error fetching {url}: {e}")

    return links


def main():
    all_links = set()

    for url in SEED_URLS:
        print(f"Scanning: {url}")
        found = extract_ats_links(url)
        all_links.update(found)
        time.sleep(1)

    print(f"Total ATS links collected: {len(all_links)}")

    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ats_url"])
        for link in sorted(all_links):
            writer.writerow([link])

    print("Saved to output.csv")


if __name__ == "__main__":
    main()

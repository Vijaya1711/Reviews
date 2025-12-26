import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import os
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def parse_capterra_date(date_str):
    return datetime.strptime(date_str, "%b %d, %Y")

def in_range_date(date_obj, start, end):
    return start <= date_obj <= end


def save_json(company, source, new_data):
    filename = "all_reviews.json"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []
    else:
        existing_data = []

    for r in new_data:
        existing_data.append({
            "company": company,
            "source": source,
            "title": r.get("title", ""),
            "review": r.get("review", ""),
            "date": r.get("date", ""),
            "rating": r.get("rating", ""),
            "reviewer": r.get("reviewer", "")
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)

    print(f"{len(new_data)} reviews saved to {filename}")



def scrape_g2(company, start, end):
    reviews = []
    page = 1

    while True:
        url = f"https://www.g2.com/products/{company}/reviews?page={page}"
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("div.paper")
        if not cards:
            break

        for c in cards:
            title = c.select_one("h3")
            body = c.select_one("p")
            date_tag = c.select_one("time")
            rating = c.select_one("span.fw-semibold")

            if not date_tag or not date_tag.has_attr("datetime"):
                continue

            review_date = parse_date(date_tag["datetime"][:10])
            if not in_range_date(review_date, start, end):
                continue

            reviews.append({
                "title": title.text.strip() if title else "",
                "review": body.text.strip() if body else "",
                "date": review_date.strftime("%Y-%m-%d"),
                "rating": rating.text.strip() if rating else "",
                "reviewer": "G2 User"
            })

        page += 1
        time.sleep(1)

    return reviews



def scrape_capterra(company, start, end):
    reviews = []
    page = 1

    while True:
        url = f"https://www.capterra.com/p/{company}/reviews/?page={page}"
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("div.review")
        if not cards:
            break

        for c in cards:
            title = c.select_one("h3")
            body = c.select_one("p")
            date_tag = c.select_one("span.review-date")
            rating = c.select_one("span.star-rating")

            if not date_tag:
                continue

            try:
                review_date = parse_capterra_date(date_tag.text.strip())
            except:
                continue

            if not in_range_date(review_date, start, end):
                continue

            reviews.append({
                "title": title.text.strip() if title else "",
                "review": body.text.strip() if body else "",
                "date": review_date.strftime("%Y-%m-%d"),
                "rating": rating.text.strip() if rating else "",
                "reviewer": "Capterra User"
            })

        page += 1
        time.sleep(1)

    return reviews



def scrape_trustradius(company, start, end):
    reviews = []
    page = 1

    while True:
        url = f"https://www.trustradius.com/products/{company}/reviews?page={page}"
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("div.review")
        if not cards:
            break

        for c in cards:
            title = c.select_one("h3")
            body = c.select_one("p")
            date_tag = c.select_one("time")
            rating = c.select_one("span.rating")

            if not date_tag or not date_tag.has_attr("datetime"):
                continue

            review_date = parse_date(date_tag["datetime"][:10])
            if not in_range_date(review_date, start, end):
                continue

            reviews.append({
                "title": title.text.strip() if title else "",
                "review": body.text.strip() if body else "",
                "date": review_date.strftime("%Y-%m-%d"),
                "rating": rating.text.strip() if rating else "",
                "reviewer": "TrustRadius User"
            })

        page += 1
        time.sleep(1)

    return reviews


def main():
    print("=== Review Scraper ===")

    try:
        company = input("Enter company name (slug): ").strip()
        source = input("Enter source (g2 / capterra / trustradius): ").strip().lower()
        start = parse_date(input("Enter start date (YYYY-MM-DD): ").strip())
        end = parse_date(input("Enter end date (YYYY-MM-DD): ").strip())
    except:
        print("Invalid input format")
        sys.exit(1)

    if start > end:
        print("Start date must be before end date")
        sys.exit(1)

    if source == "g2":
        data = scrape_g2(company, start, end)
    elif source == "capterra":
        data = scrape_capterra(company, start, end)
    elif source == "trustradius":
        data = scrape_trustradius(company, start, end)
    else:
        print("Invalid source")
        sys.exit(1)

    if not data:
        print("No reviews found in given date range")
        sys.exit(0)

    save_json(company, source, data)


if __name__ == "__main__":
    main()



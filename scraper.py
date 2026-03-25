# scraper.py
# Web Scraper — Commit 2
# Add HTML parsing using BeautifulSoup so we can
# search through the page content like a structured document.

import requests
from bs4 import BeautifulSoup

# ── Configuration ─────────────────────────────────────────────
URL = "https://news.ycombinator.com/"


# ================================================================
# fetch_page()
# Sends an HTTP GET request to the target URL.
# Returns the response object if successful.
# Returns None if something goes wrong.
# ================================================================
def fetch_page(url):
    print(f"Fetching page: {url}")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print("Page fetched successfully.\n")
            return response
        else:
            print(f"Failed. Status code: {response.status_code}")
            return None

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect. Check your internet connection.")
        return None

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Try again later.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
        return None


# ================================================================
# parse_html()
# Takes the raw HTML response and parses it with BeautifulSoup.
# "html.parser" is Python's built-in parser — no extra install.
# Returns a BeautifulSoup object we can search through cleanly.
# ================================================================
def parse_html(response):
    # BeautifulSoup turns raw messy HTML into a searchable tree
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the page title to confirm parsing is working
    page_title = soup.find("title")

    if page_title:
        print(f"Page title : {page_title.get_text()}")

    print(f"Parsing complete.\n")
    return soup


# ── Main ──────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("         PYTHON WEB SCRAPER")
    print("=" * 50 + "\n")

    # Step 1 — fetch the page
    response = fetch_page(URL)
    if response is None:
        print("Scraping stopped due to fetch error.")
        return

    # Step 2 — parse the HTML
    soup = parse_html(response)

    # Temporary: test that we can search the parsed HTML
    # Find all <a> tags and count them
    all_links = soup.find_all("a")
    print(f"[DEBUG] Total links found on page: {len(all_links)}")
    print("[DEBUG] Parsing is working correctly.")


if __name__ == "__main__":
    main()
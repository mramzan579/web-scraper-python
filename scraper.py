# scraper.py
# Web Scraper — Commit 1
# Set up the project and send a basic HTTP request
# to confirm we can connect to the target webpage.

import requests

# ── Configuration ─────────────────────────────────────────────
# The URL we want to scrape
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
        # Send the GET request with a 10 second timeout
        response = requests.get(url, timeout=10)

        # Status code 200 means the request was successful
        if response.status_code == 200:
            print("Page fetched successfully.")
            print(f"Status code : {response.status_code}")
            print(f"Content size: {len(response.text)} characters\n")
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

    # Temporary: print first 200 characters of raw HTML
    # to confirm we received real page content
    print("[DEBUG] First 200 characters of HTML:")
    print(response.text[:200])
    print("\n[DEBUG] Fetch is working correctly.")


if __name__ == "__main__":
    main()
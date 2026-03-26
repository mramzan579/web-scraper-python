# scraper.py
# Web Scraper
# Extract all article titles and their links from
# the parsed HTML using BeautifulSoup search methods.

import requests
from bs4 import BeautifulSoup

# Configuration
URL = "https://news.ycombinator.com/"



# fetch_page()
# Sends an HTTP GET request to the target URL.
# Returns the response object if successful.
# Returns None if something goes wrong.

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



# parse_html()
# Takes the raw HTML response and parses it with BeautifulSoup.
# Returns a BeautifulSoup object we can search through.

def parse_html(response):
    soup = BeautifulSoup(response.text, "html.parser")
    print("HTML parsed successfully.\n")
    return soup



# extract_data()
# Searches the parsed HTML for article titles and their links.
# Hacker News wraps each story in <span class="titleline">
# Inside that span is an <a> tag with the title and URL.
# Returns a list of dictionaries — each with a number,
# title, and link.

def extract_data(soup):
    articles = []   # empty list — we will fill this up

    # Find all elements that match this pattern:
    # <span class="titleline"> ... </span>
    title_elements = soup.find_all("span", class_="titleline")

    # If nothing found — page structure may have changed
    if not title_elements:
        print("No articles found on this page.")
        return articles

    # Loop through every title element found
    for index, element in enumerate(title_elements, start=1):

        # Inside each span find the first <a> tag
        # That <a> holds the article title and URL
        link_tag = element.find("a")

        if link_tag:
            # get_text() extracts the visible text
            title = link_tag.get_text()

            # get("href") gets the URL from the href attribute
            # "" is the default if href does not exist
            link = link_tag.get("href", "")

            # Store as a dictionary and add to the list
            articles.append({
                "number" : index,
                "title"  : title,
                "link"   : link
            })

    print(f"Extracted {len(articles)} articles.\n")
    return articles


# Main 
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

    # Step 3 — extract the data
    articles = extract_data(soup)

    if not articles:
        print("No articles to display.")
        return

    # Temporary: print first 5 articles to confirm extraction works
    print("[DEBUG] First 5 articles extracted:\n")
    for article in articles[:5]:
        print(f"{article['number']}. {article['title']}")
        print(f"   {article['link']}")
        print("-" * 50)

    print("\n[DEBUG] Extraction is working correctly.")


if __name__ == "__main__":
    main()
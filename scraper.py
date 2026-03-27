# scraper.py
# Web Scraper 
# Display all extracted articles in the terminal
# and save them to a text file called results.txt

import requests
from bs4 import BeautifulSoup

# Configuration 
URL         = "https://news.ycombinator.com/"
OUTPUT_FILE = "results.txt"


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
# Searches the parsed HTML for article titles and links.
# Returns a list of dictionaries with number, title, and link.

def extract_data(soup):
    articles = []

    title_elements = soup.find_all("span", class_="titleline")

    if not title_elements:
        print("No articles found on this page.")
        return articles

    for index, element in enumerate(title_elements, start=1):
        link_tag = element.find("a")

        if link_tag:
            title = link_tag.get_text()
            link  = link_tag.get("href", "")

            articles.append({
                "number" : index,
                "title"  : title,
                "link"   : link
            })

    print(f"Extracted {len(articles)} articles.\n")
    return articles



# save_to_file()
# Writes all extracted articles to a plain text file.
# Uses Python's built-in open() with a with statement.
# The with statement closes the file automatically when done.

def save_to_file(articles, filename):
    if not articles:
        print("Nothing to save.")
        return

    try:
        # "w" mode — write mode, creates file if it does not exist
        # encoding="utf-8" handles special characters in titles
        with open(filename, "w", encoding="utf-8") as file:

            # Write header
            file.write("=" * 50 + "\n")
            file.write("        SCRAPED ARTICLES\n")
            file.write("=" * 50 + "\n")
            file.write(f"Source : {URL}\n")
            file.write(f"Total  : {len(articles)} articles\n")
            file.write("=" * 50 + "\n\n")

            # Write each article
            for article in articles:
                file.write(f"{article['number']}. {article['title']}\n")
                file.write(f"   Link: {article['link']}\n")
                file.write("-" * 50 + "\n")

        print(f"Results saved to '{filename}' successfully.")

    except IOError as e:
        print(f"Error saving file: {e}")



# main()
# Entry point. Runs all steps in order:
#   1. Fetch the page
#   2. Parse the HTML
#   3. Extract the data
#   4. Display results in terminal
#   5. Save results to file

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
        print("No articles found. The page structure may have changed.")
        return

    # Step 4 — display all results in the terminal
    print(f"Found {len(articles)} articles:\n")
    print("-" * 50)

    for article in articles:
        print(f"{article['number']}. {article['title']}")
        print(f"   {article['link']}")
        print("-" * 50)

    # Step 5 — save results to file
    save_to_file(articles, OUTPUT_FILE)

    print(f"\nDone! Open '{OUTPUT_FILE}' to see the saved results.")
    print("=" * 50)


if __name__ == "__main__":
    main()
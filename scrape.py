import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pdfkit
import time

BASE_URL = "https://www.angelone.in/support"
visited_links = set()

def is_valid_url(url):
    """
    Checks if:
      1) The URL starts with BASE_URL,
      2) The path doesn't start with '/support/hindi',
      3) The scheme is either http or https,
      4) The URL doesn't contain 'tel:' in its path.
    """
    # Parse the URL
    parsed = urlparse(url)

    # Must be HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        return False

    # Must start with https://www.angelone.in/support
    if not url.startswith(BASE_URL):
        return False

    # Skip Hindi pages
    if parsed.path.startswith("/support/hindi"):
        return False

    # If "tel:" appears in the path, skip
    if "tel:" in parsed.path:
        return False

    return True

def get_links(url):
    """
    Fetches 'url' and returns a set of valid, normalized links.
    Skips mailto:, tel:, javascript:, and anchor (#) links before they are joined.
    """
    links = set()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return links  # Return empty if not successful

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for a_tag in soup.find_all("a", href=True):
            raw_href = a_tag["href"].strip()

            # Skip tel:, mailto:, javascript:, #, etc. right away
            if (raw_href.startswith("tel:") or 
                raw_href.startswith("mailto:") or
                raw_href.startswith("javascript:") or
                raw_href.startswith("#")):
                continue

            # Convert relative link to absolute
            full_link = urljoin(url, raw_href)
            
            # Normalize
            parsed = urlparse(full_link)
            normalized_link = parsed.scheme + "://" + parsed.netloc + parsed.path

            # Check if it's valid for our domain
            if is_valid_url(normalized_link):
                links.add(normalized_link)

    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
    return links

def crawl(url, collected_pages):
    """
    Recursively crawls pages under BASE_URL, storing HTML content in 'collected_pages'.
    Uses a depth-first approach.
    """
    if url in visited_links:
        return
    visited_links.add(url)

    try:
        print(f"Crawling: {url}")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            collected_pages[url] = response.text
            # Get child links and recurse
            child_links = get_links(url)
            for link in child_links:
                crawl(link, collected_pages)

        # Be polite: sleep briefly between requests
        time.sleep(1)

    except requests.RequestException as e:
        print(f"Failed to crawl {url}: {e}")

def main():
    collected_pages = {}
    crawl(BASE_URL, collected_pages)

    # Combine all HTML content
    combined_html = """
    <html>
      <head>
        <meta charset="utf-8">
        <title>Angel One Support</title>
      </head>
      <body>
    """

    for url, html_content in collected_pages.items():
        combined_html += f"<h1>Page: {url}</h1>\n"
        combined_html += html_content
        combined_html += "<hr/>\n"

    combined_html += "</body></html>"

    # Convert to PDF
    pdfkit.from_string(combined_html, "angelone_support_pages.pdf")
    print("PDF file 'angelone_support_pages.pdf' created successfully.")

if __name__ == "__main__":
    main()

from bs4 import BeautifulSoup
from termcolor import colored
from requests import get
from os import system


# holds all the content types for easy conversion
ALL_CONTENT_TYPES = {
    "application/javascript": "JavaScript",
    "application/ogg": "OGG (Audio)",
    "application/pdf": "PDF",
    "application/json": "JSON",
    "application/xml": "XML",
    "application/zip": "ZIP",
    "audio/mpeg": "MPEG (Audio)",
    "audio/x-wav": "WAV (Audio)",
    "image/gif": "GIF",
    "image/jpeg": "JPEG",
    "image/png": "PNG",
    "image/tiff": "TIFF",
    "image/svg+xml": "SVG",
    "text/css": "CSS",
    "text/csv": "CSV",
    "text/html": "HTML",
    "text/javascript": "JavaScript",
    "text/plain": "Plain Text (No Markup)",
    "text/xml": "XML",
    "video/mpeg": "MPEG (Video)",
    "video/mp4": "MP4 (Video)",
    "video/quicktime": "QuickTime (Video)",
    "video/webm": "WebM (Video)"
}


def load_bs4_page(url: str) -> BeautifulSoup:
    """Get page contents, load into BeautifulSoup, and return object."""
    page = get(url)
    return BeautifulSoup(page.content, "html.parser")


def get_anchor_tags(page: BeautifulSoup) -> list:
    """Return a list of all anchor tag links."""
    return [link["href"] for link in page.find_all("a")]


def get_content_type(url: str) -> str:
    """Return the page content type."""
    headers = get(url).headers

    for content_type in ALL_CONTENT_TYPES:
        if content_type in headers["Content-Type"]:
            return ALL_CONTENT_TYPES[content_type]

    # the content type wasn't found, so it's unknown
    return "undefined"


def crawl(url: str, explored: set, to_visit: set) -> str:
    """Crawl a page, add said URL to `explored` and add all links on the page
    to `to_visit` as unexplored pages."""
    page = load_bs4_page(url)
    anchors = get_anchor_tags(page)

    # get the page title and content type
    title = page.find("title").string
    content_type = get_content_type(url)

    # add the current URL to `explored` because we visited it
    explored.add(url)

    # add links to `to_visit` if and *only* if the page hasn't been explored
    # already (otherwise will be stuck in an infinite loop)
    for anchor in anchors:
        if anchor not in explored:
            to_visit.add(anchor)

    # data to be written to the CSV file
    return {
        "url": url,
        "title": title,
        "content_type": content_type
    }


def create_sitemap(start_url: str, explored: set, to_visit: set) -> dict:
    """Create the sitemap dictionary given a start URL."""
    sitemap = {}
    counter = 1

    # start the process with the first page
    index_crawl = crawl(start_url, explored, to_visit)
    sitemap[start_url] = index_crawl

    index_page_stats = f"{ counter }: { index_crawl }"
    print(colored(index_page_stats, "green"))

    counter += 1

    # while pages are yet to be explored...
    while len(to_visit) != 0:
        # get a random page and crawl it
        first_page = to_visit.pop()
        page_result = crawl(first_page, explored, to_visit)

        current_page_stats = f"{ counter }: { page_result }"

        print(colored(current_page_stats, "green"))

        sitemap[first_page] = page_result
        counter += 1

    return sitemap


def dict_to_csv(sitemap: dict) -> str:
    """Return the `sitemap` in CSV form."""
    headers = "URL,Page Title,Content Type"
    by_line = set()

    # loop through each page and write the CSV row
    for page, page_info in sitemap.items():
        title, content_type = page_info["title"], page_info["content_type"]
        row = f"{ page },{ title },{ content_type }"

        by_line.add(row)

    lines = "\n".join(by_line)
    return f"{ headers }\n{ lines }"


def save_to_csv(data: str, title: str) -> None:
    """Write the given `data` to a sitemap file named `title`."""
    system("rm sitemap.csv")

    with open(f"{ title }.csv", "w") as sitemap:
        sitemap.write(data)

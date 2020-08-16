from urllib.parse import urlsplit
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

# global start url variable
START_URL = None
START_UNPACKED = None


def split_url(url: str) -> dict:
    """Split a given URL into its scheme, base, and path."""
    unpacked = urlsplit(url)

    path, query, fragment = unpacked.path, unpacked.query, unpacked.fragment
    divider = "#" if unpacked.fragment else ""

    full_path = f"{ path }{ query }{ divider }{ fragment }"

    return {
        "scheme": unpacked.scheme,
        "base": unpacked.netloc,
        "path": full_path
    }


def get_page(url: str):
    """Fetch a `GET` request to the URL and return the parser."""
    page = get(url)
    return BeautifulSoup(page.content, "html.parser")


def is_valid(url: str) -> bool:
    """Check to see if a given URL belongs to the site we're scraping."""
    if url.startswith("/"):
        return True

    global START_URL
    global START_UNPACKED

    unpacked = split_url(url)
    return unpacked["base"] == START_UNPACKED["base"]


def fix_url(url: str) -> str:
    """Add the beginning path to a URL if only endpoint."""
    global START_UNPACKED

    if url.startswith("/"):
        scheme, base = START_UNPACKED["scheme"], START_UNPACKED["base"]
        return f"{ scheme }://{ base }{ url }"

    return url


def print_status(index: int, page_info: dict) -> None:
    """For logging purposes, print the page index and info."""
    message = f"({ index }): { page_info }"
    print(colored(message, "green"))


def get_links(page: BeautifulSoup):
    """Get all valid links on a specified page."""
    links = set()

    for link in page.find_all("a"):
        try:
            links.add(link["href"])
        except KeyError:
            message = f"This link doesn't have an `href` attribute: { link }"
            print(colored(message, "red"))

    valid_links = [link for link in links if is_valid(link)]
    return [fix_url(link) for link in valid_links]


def get_content_type(url: str) -> str:
    """Get the page's content type based on the headers."""
    global ALL_CONTENT_TYPES
    page_headers = get(url).headers

    for content_type in ALL_CONTENT_TYPES:
        if content_type in page_headers["Content-Type"]:
            return ALL_CONTENT_TYPES[content_type]

    return "undefined"


def crawl_page(url: str, explored: set, to_visit: set) -> dict:
    """Crawl a specified URL and add it to the explored."""
    page = get_page(url)
    links = get_links(page)

    other_url = f"{ url[:-1] }" if url.endswith("/") else f"{ url }/"

    # get the page title and content type
    try:
        title = page.find("title").string
    except AttributeError:
        title = url
    content_type = get_content_type(url)

    explored.add(url)
    explored.add(other_url)

    for link in links:
        if link not in explored:
            to_visit.add(link)

    return {
        "url": url,
        "title": title,
        "content_type": content_type
    }


def create_sitemap(start_url: str, explored: set, to_visit: set) -> tuple:
    """Crawl the entire website given a `start_url`."""
    global START_URL
    global START_UNPACKED

    start_url_info = split_url(start_url)
    START_URL, START_UNPACKED = start_url, start_url_info

    sitemap = {}
    counter = 1

    index = crawl_page(start_url, explored, to_visit)
    sitemap[start_url] = index

    print_status(counter, index)
    counter += 1

    while len(to_visit) != 0:
        next_page = to_visit.pop()

        crawled_page = crawl_page(next_page, explored, to_visit)
        print_status(counter, crawled_page)

        sitemap[next_page] = crawled_page
        counter += 1

    return (sitemap, counter)


def dict_to_csv(sitemap: dict) -> str:
    """Convert the sitemap dictionary to CSV text."""
    headers = "URL,Page Title,Content Type"
    result = f"{ headers }"

    for url, page_info in sitemap.items():
        title, content_type = page_info["title"], page_info["content_type"]
        line = f"{ url },{ title },{ content_type }"
        result = f"{ result }\n{ line }"

    return result


def save_to_csv(data: str, title: str) -> None:
    """Write the given `data` to a sitemap file named `title`."""
    system("rm *.csv")

    with open(f"{ title }.csv", "w") as sitemap:
        sitemap.write(data)

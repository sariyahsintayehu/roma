"""
Roma: Sitemap (in CSV form) generator to automate the senseless task of 
creating a sitemap by hand for free.

Created by Brehanu Bugg 8/14/2020.

Designed for Python 3.7.3
"""
from __future__ import print_function, unicode_literals
from utilities import create_sitemap, dict_to_csv, save_to_csv
from PyInquirer import prompt
from termcolor import colored
from time import time


# `explored` holds the URLs that have been explored already whereas `to_visit`
# denotes the pages still left un-visited
EXPLORED = set()
TO_VISIT = set()

RESPONSE = prompt([
    {
        "type": "input",
        "name": "start_url",
        "message": "What is the starting URL endpoint?"
    }
])


# denotes the first URL to crawl
START_URL = RESPONSE["start_url"]


def main():
    # for logging purposes
    start_time = time()

    # create the sitemap and convert the dictionaries to CSV
    result = create_sitemap(START_URL, EXPLORED, TO_VISIT)
    sitemap, n_pages = result[0], result[1]
    to_csv = dict_to_csv(sitemap)

    elapsed_time = time() - start_time
    stats = f"Explored { n_pages - 1 } pages in { elapsed_time } seconds"

    print(colored("=" * 50, "white"))
    print(colored(stats, "blue"))

    # write the data to a sitemap CSV file (easily exportable to Excel)
    save_to_csv(to_csv, "sitemap")

    print(colored("Successfully saved sitemap to CSV", "magenta"))


if __name__ == "__main__":
    main()

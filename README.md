# Roma: Sitemap Generator

**Problem Statement**

Sitemap generators online either cost money, don't map the entire website, or return the data in a weird format that isn't favorable to whomever uses it. The challenge for Roma was to create a free sitemap generator that parses every page and returns a CSV file with columns for the page's URL, Title, and Content Type.

**Why "Roma"?**

I made a [name generator](https://github.com/thebrehanubugg/jou) a while ago and "Roma" was entry #284. Plus, the name sounds similar/is an anagram of "roam" which essentially is what this program does... "roaming" a website for links that link back to itself to make a self-created map.

**Algorithmic Approach**

Fundamentally, this is a [search problem](https://en.wikipedia.org/wiki/Search_problem) where there are nodes (or verticies) and edges. The nodes are individual pages (such as `1.html`, `2.html`, `3.html`, etc.) and the edges are the links that go to another page under the same website base domain.

The simplest search algorithm for this program was [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search) where the crawler starts at a page, adds itself to an `explored` list, and adds all self-pointing (meaning to the same base domain) links to a `to visit` set. This algorithm differs from BFS as it choses a random page from the `to visit` queue rather than the first item (BFS uses the [FIFO](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)) method for determining the next node to explore).

Once all the pages are explored, it's quite easy to create the CSV sitemap file.

**Installation**

Download the project either from the GitHub repository or run the following command in your terminal:

`git clone https://github.com/thebrehanubugg/roma roma`

Once downloaded, change into the newly downloaded directory and run `pip3 install` to download the required dependencies for the program to work. Once complete you can run the program as outlined in the next section.

**Usage**

Once downloaded, change into the `roma` directory and run `python3 roma.py` and enter the base URL of the site you want to crawl when prompted. Each page will be printed, along with some other metadata. Once complete, the program will tell you the number of pages its crawled and a time metric measured in seconds.

Once completed, a new `sitemap.csv` will be appear in the `roma` directory that can easily be uploaded to Excel, Google Sheets, or can be manipulated more.

The structure of the CSV file has the header where the columns are `URL`, `Page Title`, and `Content Type` respectively. The first two columns are self-explanatory but `Content Type` might not.

The third column will be one of the following values:

* JavaScript,
* OGG (Audio)
* PDF
* JSON
* XML
* ZIP
* MPEG (Audio)
* WAV (Audio)
* GIF
* JPEG
* PNG
* TIFF
* SVG
* CSS
* CSV
* HTML
* JavaScript
* Plain Text (No Markup)
* XML
* MPEG (Video)
* MP4 (Video)
* QuickTime (Video)
* WebM (Video)

It essentially holds the page content's type. Some pages will be just markup or some other other type such as image or audio. The last column will specify exactly which one it is. If it can't determine the page's content type, the last column will say `undefined`.
import requests
from bs4 import BeautifulSoup

URL = "https://www.wandsworth.gov.uk/toilets"
BASE = "https://www.wandsworth.gov.uk"


# Wandsworth toilet directory too generic - just links to parks / libraries without exact specifics of where the
# toilet is located


def parse_main_page():
    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')
    divs = soup.find_all("div", {"class": "main-info"})
    links = divs[0].find_all("a")
    urls = [l['href'] for l in links]
    for i in range(len(urls)):
        u = urls[i]
        if "http" not in u:
            urls[i] = BASE + urls[i]
    print(urls)


if __name__ == "__main__":
    parse_main_page()

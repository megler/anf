import requests, re, time, random
from .models import Category
from bs4 import BeautifulSoup


# Credit: https://stackoverflow.com/questions/57019565/google-search-html-doesnt-contain-div-id-resultstats
def check_ait(kw):
    """Uses Beautiful Soup To Scrape allintitle search results. Used for golden
    ratio keyword calculations."""

    url = "https://www.google.com/search?q=allintitle:" + kw
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
    }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", id="result-stats")
    return int("".join(re.findall(r"\d+", div.text.split()[1])))

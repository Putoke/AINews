__author__ = 'joakim'

import nltk
from bs4 import BeautifulSoup
import urllib.request

baseUrl = "http://www.nytimes.com/pages/"

def main():

    subject = "politics"
    url = baseUrl + subject + "/index.html"
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page.read(), "html.parser")

    div = soup.find("div", {"class", "searchResults"})
    links = soup.find_all('a', href=True)
    articles = set([])

    for link in links:
        if "www.nytimes.com" and "2015/10" in link['href'] and not "interactive" in link['href']: articles.add(link['href'])

    print (articles)

if __name__ == "__main__":
    main()
__author__ = 'joakim'

import nltk
from bs4 import BeautifulSoup
import requests

def main():

    baseUrl = "http://www.nytimes.com/pages/"

    subject = "politics"
    url = baseUrl + subject + "/index.html"
    page = requests.get(url, timeout=5)

    soup = BeautifulSoup(page.content, "html.parser")

    div = soup.find("div", {"class", "searchResults"})
    links = soup.find_all('a', href=True)
    articleLinks = set([])

    for link in links:
        if "www.nytimes.com" in link['href'] and "com/2015/10" in link['href'] and not "interactive" in link['href']:
            articleLinks.add(link['href'])

    articles = set()

    i = 0
    for article in articleLinks:
        sida = requests.get(article, timeout=5)
        soppa = BeautifulSoup(sida.content, "html.parser")
        header = soppa.find('', {"class": "story-heading"})
        body = soppa.find('div', {"class": "story-body"})
        bodytext = soppa.find_all('p', {"class": "story-content"})
        articleText = ""
        for t in bodytext:
            articleText += t.text
        articleTuple = (header.text, articleText)
        articles.add(articleTuple)
        i = i + 1
        print ("Article: " + str(i) + "/" + str(len(articleLinks)) + " added.")

    #return articles

if __name__ == "__main__":
    main()
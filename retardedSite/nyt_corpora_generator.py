__author__ = 'joakim'

from bs4 import BeautifulSoup
import requests, sys

class NytCorporaGenerator:

    def fetchFromNytCrawler(self, subject):

        articleLinks = self.crawlTime(subject)

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

        return articles

    def crawlTime(self, subject):
        baseUrl = "http://www.nytimes.com/pages/"
        url = baseUrl + subject + "/index.html"
        page = requests.get(url, timeout=5)

        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all('a', href=True)
        articleLinks = set([])

        for link in links:
            if "www.nytimes.com" in link['href'] and "com/2015/10" in link['href'] and not "interactive" in link['href']:
                articleLinks.add(link['href'])

        return articleLinks

    def generateCorpusToFile(self, subject):
        f = open('nyt_corpus_' + subject, 'w')
        for tuple in self.fetchFromNytCrawler(subject):
            f.write(tuple[1])

    def main(self, argv):
        if len(argv) >= 1:
            for a in argv:
                self.generateCorpusToFile(a)

if __name__ == '__main__':
    NytCorporaGenerator().main(sys.argv[1:])
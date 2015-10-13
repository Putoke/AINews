__author__ = 'fredrik'

from bs4 import BeautifulSoup
import urllib.request
import nltk

class NewsParser:

    def fetchBBC(self, url):

        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), "html.parser")
        data = soup.find('div', {'class':'story-body__inner'})

        string = ""
        for asdf in data.find_all('p'):
            string += asdf.text + ' '

        return string

    def fetchFromFile(self, filename):
        f = open(filename, 'r')
        output = open('corpus', 'w')
        for line in f:
            data = self.fetchBBC(line)
            output.write(data)

    def fetchFromNytCrawler(self, subject):
        page = urllib.request.urlopen('http://www.nytimes.com/2015/10/14/technology/twitter-to-cut-more-than-300-jobs.html?ref=technology')
        soup = BeautifulSoup(page.read(), "html.parser")
        data = soup.find('div', {'class':'story-body'})

        string = ""
        for asdf in data.find_all('p'):
            string += asdf.text + ' '

        return string

    def crawlTime(self, subject):
        baseUrl = "http://www.nytimes.com/pages/"
        url = baseUrl + subject + "/index.html"
        page = urllib.request.urlopen(url)

        soup = BeautifulSoup(page.read(), "html.parser")

        div = soup.find("div", {"class", "searchResults"})
        links = soup.find_all('a', href=True)
        articles = set([])

        for link in links:
            if "www.nytimes.com" and "2015/10" in link['href'] and not "interactive" in link['href']: articles.add(link['href'])

        return articles

    def test(self):

        f = open('corpus', 'r')

        content = f.readline()

        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        tokenized_content = tokenizer.tokenize(content)

        #tagged = nltk.pos_tag(tokenized_content)

        content_model = nltk.

        return ''






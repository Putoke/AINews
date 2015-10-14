__author__ = 'fredrik'

from bs4 import BeautifulSoup
import urllib.request
import nltk
import requests
import random

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

    def corpusFromCrawler(self, subject):
        f = open('nyt_corpus', 'w')
        for tuple in self.fetchFromNytCrawler(subject):
            f.write(tuple[1])
        return

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

    def test(self):

        f = open('nyt_corpus', 'r')

        content = f.readline()

        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        tokenized_content = tokenizer.tokenize(content)
        ngrams = list(nltk.ngrams(tokenized_content, 3))

        cache = self.db(ngrams)
        #return tokenized_content
        return self.generate_text(100, cache, tokenized_content)

    def db(self, ngrams):
        cache = {}
        for w1, w2, w3 in ngrams:
            key = (w1, w2)
            if key in cache:
                cache[key].append(w3)
            else:
                cache[key] = []
                cache[key].append(w3)

        return cache

    def generate_text(self, size, cache, tokenized_content):
        seed = random.randint(0, len(tokenized_content)-3)
        w1, w2 = tokenized_content[seed], tokenized_content[seed+1]
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            #print(cache[(w1, w2)])
            w1, w2 = w2, random.choice(cache[(w1, w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)

    #finder = nltk.QuadgramCollocationFinder.from_words(tokenized_content)
        #scored = finder.score_ngrams(nltk.collocations.TrigramAssocMeasures.raw_freq)
        #set(trigram for trigram, score in scored) == set(nltk.trigrams(tokenized_content))
        #tagged = nltk.pos_tag(tokenized_content)

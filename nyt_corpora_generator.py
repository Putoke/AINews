from bs4 import BeautifulSoup
import requests, sys
import re


class NytCorporaGenerator:

    def fetch_from_nyt_crawler(self, subject):

        article_links = self.crawl_time(subject)

        articles = set()

        i = 0
        for article in article_links:
            page = requests.get(article, timeout=5)
            soup = BeautifulSoup(page.content, "html.parser")
            header = soup.find('', {"class": "story-heading"})
            body = soup.find('div', {"class": "story-body"})
            body_text = soup.find_all('p', {"class": "story-content"})

            article_text = ""
            for t in body_text:

                asdf = re.sub(r"“|”", "", t.text)
                article_text += asdf + ' '


            article_tuple = (header.text, article_text)
            articles.add(article_tuple)
            i += 1
            print("Article: " + str(i) + "/" + str(len(article_links)) + " added.")

        return articles

    def crawl_time(self, subject):
        base_url = "http://www.nytimes.com/pages/"
        url = base_url + subject + "/index.html"
        page = requests.get(url, timeout=5)

        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all('a', href=True)
        article_links = set([])

        for link in links:
            if "www.nytimes.com" in link['href'] and "com/2015/10" in link['href'] and not "interactive" in link['href']:
                article_links.add(link['href'])

        return article_links

    def generate_corpus_to_file(self, subject):
        f = open('nyt_corpus_' + subject, 'w')
        f_headlines = open('nyt_corpus_' + subject + '_headlines', 'w')
        for article in self.fetch_from_nyt_crawler(subject):
            f_headlines.write(article[0] + " ")
            f.write(article[1] + " ")



    def main(self, argv):
        if len(argv) >= 1:
            for a in argv:
                self.generate_corpus_to_file(a)

if __name__ == '__main__':
    NytCorporaGenerator().main(sys.argv[1:])
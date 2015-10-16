from bs4 import BeautifulSoup
import requests, sys
import re
import pickle, nltk


class NytCorporaGenerator:

    #This function looks at articles on nytimes.com under the given subject and returns an article with its headline
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

    #This function collects a list of article links from the nytimes.com site under a specific subject
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

    #This function saves the corpuses to files
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
                self.tag_corpus('nyt_corpus_' + a)
                self.tag_corpus('nyt_corpus_' + a + '_headlines')

    #This method loads a corpus and tags all words with part of speech tags and saves them to a filename_tagged file
    @staticmethod
    def tag_corpus(filename):
        f = open(filename, 'r')
        f.seek(0)
        data = f.read()
        words = nltk.word_tokenize(data)
        f.close()
        tagged_words = nltk.pos_tag(words)
        fi = open(filename+'_tagged', 'wb')
        pickle.dump(tagged_words, fi)
        fi.close()

if __name__ == '__main__':
    NytCorporaGenerator().main(sys.argv[1:])
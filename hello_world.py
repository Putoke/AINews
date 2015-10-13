__author__ = 'joakim'

import nltk
from bs4 import BeautifulSoup
import urllib.request
from parser import NewsParser


def main():

    parser = NewsParser()
    #parser.fetchFromFile('articles')

    #print(parser.fetchFromNytCrawler('asdf'))
    print(parser.test())


if __name__ == "__main__":
    main()
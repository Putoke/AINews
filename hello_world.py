__author__ = 'joakim'

import nltk
from bs4 import BeautifulSoup
import urllib.request
from parser import NewsParser
from mgen import MGen


def main():

    parser = NewsParser()
    #parser.corpusFromCrawler('business')
    #print(parser.test())

    nparser = MGen('corpus',2)

    #f = open('test.out', 'w')
    #f.write(nparser.generate(100))
    print(nparser.test())




if __name__ == "__main__":
    main()
#bajs
__author__ = 'joakim'

import nltk
from bs4 import BeautifulSoup
import urllib.request


def main():

    url = "http://www.bbc.com/news/technology-34504319"
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page.read(), "html.parser")



    print(soup.title.string)


if __name__ == "__main__":
    main()
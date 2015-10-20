Generate corpus:
To generate a corpus run the file nyt_corpora_generator.py with the following command:
python nyt_corpora_generator.py <subject>

Not every subject will work, but here are some examples:
technology, sports, business, arts

The program will generate four files with these names:
nyt_corpus_<subject>
nyt_corpus_<subject>_tagged
nyt_corpus_<subject>_headlines
nyt_corpus_<subject>_headlines_tagged

Run the text generator:
To run the text generator you will need to have a tagged corpus file and a corresponding headlines corpus which also is tagged.
The command to run it is as follows:
python gen_article.py nyt_corpus_<subject>_tagged <n-gram> <length_of_article>
The program will find the headlines file automatically. An example run:
python gen_article.py nyt_corpus_technology_tagged 3 100
This will generate a news text about technology with 3-grams and the length of the article will be 100.
The first line in the output will be the headline and the second line the body of the article.


Note:
The program has only been tested in a python 3.4 environment and is suggested to run under that version. It also has
some dependencies which has to be installed for the program to run. These are nltk, requests, beautifulsoup4 which can
be install with pip install. There are also some packages that might need to be downloaded with the nltk.download() function.
These are punkt and averaged_perceptron_tagger.
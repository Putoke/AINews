__author__ = 'fredrik'
from collections import defaultdict
import nltk
import random


class MGen:

    def __init__(self, corpus_filename,n):
        self.n = n
        self.corpus_file = open(corpus_filename)
        self.corpus_data = self.corpus_file.read()
        self.corpus_words = self.corpus_data.split()
        self.ngrams = self.create_ngrams(n)
        self.cache = self.create_cache()



    def create_cache(self):
        cache = defaultdict(list)
        for wlist in self.ngrams:
            last_word = wlist[self.n-1]
            cache[tuple(wlist[x] for x in range(self.n-1))].append(last_word)
            nltk.probability.LidstoneProbDist

        return cache



    def create_ngrams(self, n):
        ngrams = list(nltk.ngrams(self.corpus_words, n))
        return ngrams

    def generate(self, length):
        seed = random.randint(0, len(self.corpus_words)-self.n)
        output = [self.corpus_words[seed +x] for x in range(self.n-1)]
        for x in range (self.n-1, length):
            next_key = tuple(output[-(self.n-1):])
            output.append(random.choice(self.cache[next_key]))

        return " ".join(output)

    def test(self):

        cfd = nltk.probability.ConditionalFreqDist(nltk.bigrams(self.corpus_words))
        cpd = nltk.probability.ConditionalProbDist(cfd, nltk.MLEProbDist)

        print(cfd)
        print(cpd['to'].prob('elect'))
        print(cpd['to'].generate())

        est = lambda cfd, bins: nltk.LidstoneProbDist(cfd, 0.2)

        print(est)

        return ''

    def test2(self):
        tags = nltk.tag.pos_tag(self.corpus_words)
        tag_set = list(set([tag for (word, tag) in tags]))
        print(len(tag_set))
        symbols = list(set([word for (word,tag) in tags]))
        print(len(symbols))

        trainer = nltk.HiddenMarkovModelTrainer(tag_set, symbols)



        trainer.train_supervised()
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

        grams = nltk.ngrams(self.corpus_words,3)


        tempgrams = defaultdict(list)
        for (a,b,c) in grams:
            tempgrams[(a,b)].append(c)




        cfd = nltk.probability.ConditionalFreqDist(tempgrams)



        #fd = nltk.probability.FreqDist(nltk.trigrams(self.corpus_words))
        #ld = nltk.probability.LidstoneProbDist(fd,0.2)

        cpd = nltk.probability.ConditionalProbDist(cfd, nltk.probability.LidstoneProbDist, 0.2)
        #cpd = nltk.probability.ConditionalProbDist(cfd, nltk.probability.MLEProbDist)



        tagged = nltk.pos_tag(self.corpus_words)
        print(tagged)

        #force | its work


        #print(cfd)
        #print(cpd[cpd.conditions()[random.randint(0,len(cpd.conditions()))]].generate())

        gen_words = []
        first_word = random.choice(list(cpd.conditions()))
        gen_words.append(first_word)
        for i in range(100):
            next_word = cpd[first_word].generate()
            gen_words.append(next_word)
            first_word = next_word
        #print(cpd['was'].prob('named'))




        return ' '.join(gen_words)
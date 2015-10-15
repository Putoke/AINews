import random, nltk, itertools
from collections import Counter, defaultdict
import pickle
import re
from nltk.tag import StanfordNERTagger

class Markov(object):

    def __init__(self, corpus_file, chain_size=3):
        self.chain_size = chain_size
        self.dictionary = defaultdict(list)
        self.corpus_file = corpus_file
        self.tagged_words = [(t[0].lower(),t[1]) for t in self.load_tagged_file(corpus_file)]
        self.words, self.pos = zip(*[(t[0], t[1]) for t in self.tagged_words])
        self.n_grams = self.create_n_grams()
        self.word_size = len(self.words)
        self.create_dictionary()
        self.x = 0

    def words_at_position(self, i):
        chain = []
        for chain_index in range(0, self.chain_size):
            chain.append(self.words[i + chain_index])
        return chain

    def create_n_grams(self):
        return list(nltk.ngrams(self.tagged_words, self.chain_size))

    def create_dictionary(self):
        for gram in self.n_grams:
            last_word = gram[self.chain_size-1]
            self.dictionary[tuple(gram[x][0] for x in range(self.chain_size-1))].append(last_word)

    def generate_markov_text(self, smoothing_function, size=25, is_headline=False):
        seed = random.randint(0, self.word_size - 3)
        while self.tagged_words[seed][1] != 'DT' and self.tagged_words[seed][0] == "." and self.tagged_words[seed][0] == ",": #Always start on a DT word
            seed = random.randint(0, self.word_size - 3)
        gen_words = []
        final_words = []
        seed_words = self.words_at_position(seed)[:-1]
        seed_words[0].title()
        gen_words.extend(seed_words)
        for i in range(size):
            last_word_len = self.chain_size - 1
            last_words = gen_words[-1 * last_word_len:]
            words_smoothed = smoothing_function(self.dictionary[tuple(last_words)])
            next_word = self.pick_next_word(words_smoothed)
            gen_words.append(next_word[0])
            if last_words[len(last_words)-1] == "." or last_words[len(last_words)-1] == "?":
                final_words.append(next_word[0].title())
            elif next_word[1] == "NNP":
                final_words.append(next_word[0].title())
            elif next_word[1] != "-NONE-":
                final_words.append(next_word[0])

        final_words[0] = final_words[0].title()

        final_text = ' '.join(final_words)
        if not is_headline:
            last_dot = final_text.rfind(".")
            final_text = final_text[:-(len(final_text)-last_dot-1)]

        final_text = final_text.replace(" ,", ",")
        final_text = final_text.replace(" .", ".")
        final_text = final_text.replace(" ?", "?")
        final_text = final_text.replace(" ’ ", "’")
        final_text = final_text.replace(" i ", " I ")
        final_text = final_text.replace(" i,", " I,")
        final_text = re.sub(r"i\'", "I'", final_text)
        final_text = re.sub(r"“|”", "", final_text)
        final_text = re.sub(r"\(|\)", "", final_text)
        final_text = re.sub(r"\s\s", " ", final_text)

        #check for dots and uppercase

        return final_text

    def add_one_smoothing(self, words):
        counted_words = Counter(words)
        for element in counted_words:
            counted_words[element] += 1
        return counted_words

    def lidstone_smoothing(self, words):
        counted_words = Counter(words)
        for element in counted_words:
            counted_words[element] *= 10
            counted_words[element] += 2
        return counted_words

    def pick_next_word(self, counted_words):
        index = random.randrange(sum(counted_words.values()))
        return next(itertools.islice(counted_words.elements(), index, None))

    @staticmethod
    def tag_corpus(filename):
        f = open(filename, 'r')
        f.seek(0)
        data = f.read()
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        words = tokenizer.tokenize(data)
        f.close()
        tagged_words = nltk.pos_tag(words)
        fi = open(filename+'_tagged', 'wb')
        pickle.dump(tagged_words, fi)
        fi.close()

    def load_tagged_file(self, filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data

if __name__ == '__main__':
    Markov.tag_corpus("retardedSite/nyt_corpus_business_head")
    #markov = Markov("retardedSite/nyt_corpus_business_head_tagged", 4)
    #print(markov.generate_markov_text(markov.add_one_smoothing, 10, True))

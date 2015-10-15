import random, nltk, itertools
from collections import Counter
import pickle


class Markov(object):

    def __init__(self, open_file, chain_size=3):
        self.chain_size = chain_size
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        words = tokenizer.tokenize(data)
        return words

    def words_at_position(self, i):
        chain = []
        for chain_index in range(0, self.chain_size):
            chain.append(self.words[i + chain_index])
        return chain

    def chains(self):
        if len(self.words) < self.chain_size:
            return

        for i in range(len(self.words) - self.chain_size - 1):
            yield tuple(self.words_at_position(i))

    def database(self):
        for chain_set in self.chains():
            key = chain_set[:self.chain_size - 1]
            next_word = chain_set[-1]
            if key in self.cache:
                self.cache[key].append(next_word)
            else:
                self.cache[key] = [next_word]

    def generate_markov_text(self, smoothing_function, size=25):
        seed = random.randint(0, self.word_size - 3)
        gen_words = []
        seed_words = self.words_at_position(seed)[:-1]
        gen_words.extend(seed_words)
        for i in range(size):
            last_word_len = self.chain_size - 1
            last_words = gen_words[-1 * last_word_len:]
            words_smoothed = smoothing_function(self.cache[tuple(last_words)])
            next_word = self.pick_next_word(words_smoothed)
            gen_words.append(next_word)
        return ' '.join(gen_words)

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




class POS():



    def __init__(self, corpus_file):
        self.corpus_file = corpus_file
        self.tagged_words = [(t[0],t[1]) for t in self.load_tagged_file(corpus_file)]
        self.words, self.pos = zip(*[(t[0], t[1]) for t in self.tagged_words])

        self.x = 0

    def tag_corpus(self, filename):
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

        #def get_words_pos(self, pos):





if __name__ == '__main__':
    #markov = Markov(open("nyt_corpus_technology"), 4)
    #print(markov.generate_markov_text(100))
    #markov.tag_corpus('nyt_corpus_technology')

    pos = POS('nyt_corpus_technology_tagged')
    print(pos.words)
    print(pos.pos)
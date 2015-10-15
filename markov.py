import random, nltk, itertools
from collections import Counter, defaultdict
import pickle
from nltk.parse.generate import demo_grammar

class Markov(object):

    def __init__(self, corpus_file, chain_size=3):
        self.chain_size = chain_size
        self.dictionary = defaultdict(list)
        self.corpus_file = corpus_file
        self.tagged_words = [(t[0],t[1]) for t in self.load_tagged_file(corpus_file)]
        self.words, self.pos = zip(*[(t[0], t[1]) for t in self.tagged_words])
        self.n_grams = self.create_n_grams()
        self.word_size = len(self.words)
        self.create_dictionary()
        self.x = 0

        self.chunker = nltk.RegexpParser('''
        NP: {<DT>? <JJ>* <NN>*} # NP
        P: {<IN>}           # Preposition
        V: {<V.*>}          # Verb
        PP: {<P> <NP>}      # PP -> P NP
        VP: {<V> <NP|PP>*}  # VP -> V (NP|PP)*
        ''')
        asd = self.chunker.parse(self.tagged_words[:20])

        #print(Counter(self.test_dict[('may', 'have')]))

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

    def create_n_grams(self):
        return list(nltk.ngrams(self.tagged_words, self.chain_size))

    def create_dictionary(self):
        for gram in self.n_grams:
            last_word = gram[self.chain_size-1]
            self.dictionary[tuple(gram[x][0] for x in range(self.chain_size-1))].append(last_word)

    def generate_markov_text(self, smoothing_function, size=25):
        seed = random.randint(0, self.word_size - 3)
        gen_words = []
        seed_words = self.words_at_position(seed)[:-1]
        gen_words.extend(seed_words)
        for i in range(size):
            last_word_len = self.chain_size - 1
            last_words = gen_words[-1 * last_word_len:]
            words_smoothed = smoothing_function(self.dictionary[tuple(last_words)])
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
        return next(itertools.islice(counted_words.elements(), index, None))[0]

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
    markov = Markov("retardedSite/A_Game_of_Thrones.txt_tagged", 3)
    print(markov.generate_markov_text(markov.lidstone_smoothing, 100))
    tmp = []
    for asd in markov.tagged_words:
        if asd[0] == "a" or asd[0] == "an":
            tmp.append(asd[1])
    #print(Counter(tmp)) #All non-tagged strings

    #print(markov.generate_markov_text(markov.add_one_smoothing, 100))
    #markov.tag_corpus('nyt_corpus_technology')
    #Markov.tag_corpus('../nyt_corpus_technology')
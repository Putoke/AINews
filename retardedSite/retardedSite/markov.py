import random, nltk


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

    def generate_markov_text(self, size=25):
        seed = random.randint(0, self.word_size - 3)
        gen_words = []
        seed_words = self.words_at_position(seed)[:-1]
        gen_words.extend(seed_words)
        for i in range(size):
            last_word_len = self.chain_size - 1
            last_words = gen_words[-1 * last_word_len:]
            next_word = random.choice(self.cache[tuple(last_words)])
            gen_words.append(next_word)
        return ' '.join(gen_words)

if __name__ == '__main__':
    markov = Markov(open("../nyt_corpus_technology"), 4)
    print(markov.generate_markov_text(100))
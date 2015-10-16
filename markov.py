import random, nltk, itertools
from collections import Counter, defaultdict
import pickle
import re
import string


class Markov(object):

    #Init all necessary variables
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

    #Returns words next to each other starting from i, where the number of words are equal to chain_size
    def words_at_position(self, i):
        chain = []
        for chain_index in range(0, self.chain_size):
            chain.append(self.words[i + chain_index])
        return chain

    #Creates the n_grams with nltk's built in function
    def create_n_grams(self):
        return list(nltk.ngrams(self.tagged_words, self.chain_size))

    #Creates the dictionary that will be used to generate the text from.
    #The structure is like this (with a bigram as an example): {('have', 'prohibited'): [('them', 'PRP')] ... }
    def create_dictionary(self):
        for gram in self.n_grams:
            last_word = gram[self.chain_size-1]
            self.dictionary[tuple(gram[x][0] for x in range(self.chain_size-1))].append(last_word)

    #The function that actually generates the body of the article
    def generate_markov_text(self, smoothing_function, size=25):
        seed = random.randint(0, self.word_size - 3)
        while self.tagged_words[seed][1] != 'DT' or self.tagged_words[seed][0] == "." or self.tagged_words[seed][0] == ",": #Always start on a DT word
            seed = random.randint(0, self.word_size - 3)
        gen_words = []
        final_words = []
        seed_words = self.words_at_position(seed)[:-1]
        seed_words[0].capitalize()
        gen_words.extend(seed_words)
        final_words.extend(seed_words)

        for i in range(size):
            last_word_len = self.chain_size - 1
            last_words = gen_words[-1 * last_word_len:]

            words_smoothed = smoothing_function(self.dictionary[tuple(last_words)])
            next_word = self.pick_next_word(words_smoothed)
            gen_words.append(next_word[0])
            if last_words[-1] == "." or last_words[-1] == "?":
                final_words.append(next_word[0].capitalize())
            elif next_word[1] == "NNP" and last_words[0] != "’":
                final_words.append(next_word[0].capitalize())
            elif next_word[1] != "-NONE-":
                final_words.append(next_word[0])

        final_words[0] = final_words[0].capitalize()

        final_text = ' '.join(final_words)
        last_dot = final_text.rfind(".")
        final_text = final_text[:-(len(final_text)-last_dot-1)]
        headline = self.generate_headline(smoothing_function)
        return headline + "\n" + self.smooth_string(final_text)

    #The function that generates the headline of the article
    def generate_headline(self, smoothing_function):
        seed = random.randint(0, self.word_size - 3)
        while self.tagged_words[seed][1] != 'DT' or self.tagged_words[seed][0] == "." or self.tagged_words[seed][0] == ",": #Always start on a DT word
            seed = random.randint(0, self.word_size - 3)
        gen_words = []
        final_words = []
        seed_words = self.words_at_position(seed)[:-1]
        gen_words.extend(seed_words)
        final_words.extend(seed_words)
        i = 0
        tag = ""
        while i < 7 or (tag != "NN" and tag != "NNS" and tag != "NNP"):
            last_word_len = self.chain_size - 1
            last_words = gen_words[-1 * last_word_len:]

            words_smoothed = smoothing_function(self.dictionary[tuple(last_words)])
            next_word = self.pick_next_word(words_smoothed)
            gen_words.append(next_word[0])
            if last_words[-1] == "." or last_words[-1] == "?":
                final_words.append(next_word[0])
            elif next_word[1] == "NNP" and last_words[0] != "’":
                final_words.append(next_word[0])
            elif next_word[1] != "-NONE-":
                final_words.append(next_word[0])
            i += 1
            tag = next_word[1]

        final_text = ' '.join(final_words)
        first_comma = final_text.find(",")
        final_text = final_text[:first_comma]
        first_dot = final_text.find(".")
        final_text = final_text[:first_dot]
        return (string.capwords(self.smooth_string(final_text)))

    #Makes the final text look a bit nicer. E.g. removes whitespaces before commas.
    def smooth_string(self, string):
        string = string.replace(" ,", ",")
        string = string.replace(" .", ".")
        string = string.replace(" ?", "?")
        string = string.replace(" !", "!")
        string = string.replace(" :", ":")
        string = string.replace(" ;", ";")
        string = string.replace(" ’ ", "’")
        string = string.replace("$ ", "$")
        string = string.replace(" i ", " I ")
        string = string.replace(" i,", " I,")
        string = re.sub(r"i\’", "I’", string)
        string = re.sub(r"“|”", "", string)
        string = re.sub(r"\(|\)", "", string)
        string = re.sub(r"\s\s", " ", string)
        return string

    #Smooths the outcome of the words with the add one smoothing technique
    def add_one_smoothing(self, words):
        counted_words = Counter(words)
        for element in counted_words:
            counted_words[element] += 1

        return counted_words

    #Smooths the outcome of the words with the lidstone smoothing technique
    def lidstone_smoothing(self, words):
        counted_words = Counter(words)
        for element in counted_words:
            counted_words[element] *= 10
            counted_words[element] += 2
        return counted_words

    #Picks the next word to add to the text
    def pick_next_word(self, counted_words):
        index = random.randrange(sum(counted_words.values()))
        return next(itertools.islice(counted_words.elements(), index, None))

    #This method loads a corpus and tags all words with part of speech tags and saves them to a filename_tagged file
    @staticmethod
    def tag_corpus(filename):
        f = open(filename, 'r')
        f.seek(0)
        data = f.read()
        words = nltk.word_tokenize(data)
        f.close()
        tagged_words = nltk.pos_tag(words)
        fi = open(filename+'_tagged', 'wb')
        pickle.dump(tagged_words, fi)
        fi.close()

    #This function loads a tagged file
    def load_tagged_file(self, filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data

if __name__ == '__main__':
    #Markov.tag_corpus("nyt_corpus_technology_headlines")
    #Markov.tag_corpus("nyt_corpus_technology")
    markov = Markov("nyt_corpus_technology_tagged", 3)
    print(markov.generate_markov_text(markov.add_one_smoothing, 25))
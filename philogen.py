import re
import sys
import os
import string
from collections import defaultdict
from random import random


#Typical sampling from a categorical distribution
def sample(items):
    next_word = None
    t = 0.0
    for k, v in items:
        t += v
        if t and random() < v/t:
            next_word = k
    return next_word


class PhiloGen:
    def __init__(self, lookback=2):
        self.lookback = lookback
        self.markov_map = defaultdict(lambda:defaultdict(int))
        self.titles = []
        
        # Gather all sources
        folder = 'sources/'
        for filename in os.listdir(folder):
            with open(folder + filename, 'r') as f:
                read_data = f.read()

            self.titles = list(
                set(self.titles).union(set(read_data.split("\n"))))
                
        print "Creating generator with {} sources and lookback {}".format(
            len(self.titles), lookback)

        # Generate map in the form:
        # (word1) -> (word2) -> (occurences of word2 after word1)
        for title in self.titles[:-1]:
            title = title.split()
            if len(title) > self.lookback:
                for i in xrange(len(title)+1):
                    word1 = ' '.join(title[max(0, i - self.lookback):i])
                    word2 = ' '.join(title[i:i+1])
                    self.markov_map[word1][word2] += 1

        # Convert map to the form:
        # (word1) -> (word2) -> (probability of word2 after word1)
        for word, following in self.markov_map.items():
            total = float(sum(following.values()))
            for key in following:
                following[key] /= total

    def gen(self, num=8):
        """Generate a number of resolutions"""
        
        sentences = []
        while len(sentences) < num:
            sentence = []
            next_word = sample(self.markov_map[''].items())

            while next_word != '':
                sentence.append(next_word)
                word1_map = self.markov_map[' '.join(sentence[-self.lookback:])]
                next_word = sample(word1_map.items())

            sentence = ' '.join(sentence)
            sent_comp = sentence.lower().translate(None, string.punctuation)
            flag = True
            for title in self.titles:
                #Prune titles that are substrings of actual titles
                title_comp = title.lower().translate(None, string.punctuation)
                if sent_comp in title_comp:
                    flag = False
                    break
            if flag:
                sentence = sentence.capitalize()
                if sentence[-1] not in string.punctuation:
                    sentence += '.'
                sentence = sentence.replace(' i ', ' I ')
                sentences.append(sentence)
        
        return sentences

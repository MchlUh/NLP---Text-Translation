import xml.etree.ElementTree as etree
import os
import unicodedata
import re


training_files_en = ['data/en-fr/IWSLT14.TED.dev2010.en-fr.en.xml', 'data/en-fr/IWSLT14.TED.tst2010.en-fr.en.xml', ]
training_files_fr = ['data/en-fr/IWSLT14.TED.dev2010.en-fr.fr.xml', 'data/en-fr/IWSLT14.TED.tst2010.en-fr.fr.xml', ]

testing_files_en = ['data/en-fr/IWSLT14.TED.tst2011.en-fr.en.xml', 'data/en-fr/IWSLT14.TED.tst2012.en-fr.en.xml', ]
testing_files_fr = ['data/en-fr/IWSLT14.TED.tst2011.en-fr.fr.xml', 'data/en-fr/IWSLT14.TED.tst2012.en-fr.fr.xml', ]


def read_file(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()
    src = root.find('srcset')
    if src is None:
        src = root.find('refset')
    if src is None:
        raise TypeError('Could not properly parse input file')
    docs = src.iterfind('doc')

    sentences = []
    for doc in docs:
        for sentence in doc.iterfind('seg'):
            sentences.append(sentence.text)

    return sentences


def make_training_pairs(path = os.path.abspath(os.getcwd())):
    sentences_fr = []
    sentences_en = []

    for file in training_files_fr:
        sentences_fr.extend(read_file(path + file))
    for file in training_files_en:
        sentences_en.extend(read_file(path + file))

    return list(zip(sentences_fr, sentences_en))


def make_testing_pairs(path = os.path.abspath(os.getcwd())):
    sentences_fr = []
    sentences_en = []

    for file in testing_files_fr:
        sentences_fr.extend(read_file(path + file))
    for file in testing_files_en:
        sentences_en.extend(read_file(path + file))

    return list(zip(sentences_fr, sentences_en))



SOS_token = 0
EOS_token = 1


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )



def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s



def readLangs(lang1, lang2, data, reverse=False):
    print("Reading lines...")

    lines = data

    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l] for l in lines]

    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs


def filterPair(p,  MAX_LENGTH):
    return len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH


def filterPairs(pairs, MAX_LENGTH):
    return [pair for pair in pairs if filterPair(pair, MAX_LENGTH)]


import xml.etree.ElementTree as etree

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


def make_training_pairs():
    sentences_fr = []
    sentences_en = []

    for file in training_files_fr:
        sentences_fr.extend(read_file(file))
    for file in training_files_en:
        sentences_en.extend(read_file(file))

    return list(zip(sentences_fr, sentences_en))


def make_testing_pairs():
    sentences_fr = []
    sentences_en = []

    for file in testing_files_fr:
        sentences_fr.extend(read_file(file))
    for file in testing_files_en:
        sentences_en.extend(read_file(file))

    return list(zip(sentences_fr, sentences_en))


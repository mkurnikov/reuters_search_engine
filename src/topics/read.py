import time
before = time.time()

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

from src.engine.parsers.reuters import ReutersParser
from src.engine.preprocess import preprocess_body, preprocess_body_lda
import settings

print(time.time() - before)
parser = ReutersParser(settings.DATA_FOLDER)
documents = []
for i, article in enumerate(parser.parse()):
    if i % 1000 == 0:
        print(i)
    documents.append(preprocess_body_lda(article['body']).split())

import pickle
with open(settings.DOCUMENTS_LIST_PKL, 'w') as pkl_out:
    pickle.dump(documents, pkl_out)

from gensim import corpora
dictionary = corpora.Dictionary(documents)
# dictionary.filter_extremes()
dictionary.save(settings.DICTIONARY)
# print dictionary[:2]

corpus = [dictionary.doc2bow(document) for document in documents]
corpora.MmCorpus.serialize(settings.CORPUS, corpus)

# print corpus[:2]







from __future__ import division, absolute_import, print_function, unicode_literals

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pickle
import settings

from gensim import corpora, models

with open(settings.DOCUMENTS_LIST_PKL, 'r') as pkl_out:
    documents = pickle.load(pkl_out)

import numpy as np
documents = np.array(documents)
# from collections import defaultdict
# word_count = defaultdict(int)
# for document in documents:
#     for word in document:
#         word_count[word] += 1
#
# bad_words = [word for word, count in word_count.items() if count <= 2]

dictionary = corpora.Dictionary.load(settings.DICTIONARY)
# dictionary.filter_extremes(no_above=1.0, no_below=0, keep_n=None)
# dictionary.compactify()
corpus = corpora.MmCorpus(settings.CORPUS) #37000

#
# tfidf = models.TfidfModel(corpus, id2word=dictionary, dictionary=dictionary, normalize=True)
# tfidf.save(settings.TF_IDF_MODEL)
# query = 'oil and gas'
# from src.engine.preprocess import preprocess_body_lda
# query = preprocess_body_lda(query)
# corpus_query = [dictionary.doc2bow(query.split(" "))]
# transformed = tfidf[corpus_query]
#
# logentropy = models.LogEntropyModel(tfidf[corpus], id2word=dictionary, normalize=True)
# logentropy.save(settings.LOGENTROPY_MODEL)

# logentropy_query = logentropy[transformed]
lsi = models.LdaModel(corpus, id2word=dictionary, num_topics=30, passes=3, alpha='auto', chunksize=4000)
lsi.save(settings.LDA_MODEL)

lsi = models.LdaModel.load(settings.LDA_MODEL)
from gensim.similarities import MatrixSimilarity
similarity_matrix = MatrixSimilarity(lsi[corpus], num_features=100)
similarity_matrix.save(settings.SIMILARITY_MATRIX)

# similarities = similarity_matrix.get_similarities(lsi[logentropy_query])

#
#
#

# lsi_query = lsi[logentropy_query]
from gensim import matutils

# matutils.cossim(lsi.)


# passes = 1, per = 11000; alpha='auto', per=9200
# passes = 2, per = 5100; alpha='auto', per=3200
# passes = 3. per = 4400; alpha='auto', per=2000

# passes = 5, per = ; per = 1708

# 50, passes = 3, per = 5400
# 50. passes = 5, per = 3428
# 50, passes = 8, 2891

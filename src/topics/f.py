from __future__ import division, absolute_import, print_function, unicode_literals

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.random_projection import sparse_random_matrix
import pickle
from gensim import models, corpora

import settings

documents = pickle.load(open(settings.DOCUMENTS_LIST_PKL))
documents = [" ".join(document) for document in documents]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)
pickle.dump(vectorizer, open(settings.VECTORIZER_LSI, 'w'))
lsa = TruncatedSVD(n_components=500)
X = lsa.fit_transform(X)
pickle.dump(lsa, open(settings.LSI_MODEL, 'w'))

X = Normalizer().fit_transform(X)
pickle.dump(X, open(settings.DOCUMENTS_LSI, 'w'))

from src.engine.preprocess import preprocess_body_lda
query = 'bank bank bank'
query = vectorizer.transform([preprocess_body_lda(query)])
query = lsa.transform(query)
query = Normalizer().fit_transform(query)
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

print(np.argsort(cosine_similarity(query, X)).shape)
# print(cosine_similarity(np.concatenate((query, X))))
# dictionary = corpora.Dictionary.load(settings.DICTIONARY)
# corpus = [dictionary.doc2bow(document) for document in pickle.load(open(settings.DOCUMENTS_LIST_PKL))]

# lsi = models.LsiModel.load(settings.LSI_MODEL)
# for document in corpus:
#     words = dict(document)
#     index = words.keys()
#     document_sparse = np.zeros((len(dictionary),), dtype=np.float32)
#     document_sparse[index] = 1

#
#
# import numpy as np
# X = np.array(corpus)
#
# # bow_repr = models.mow
#
# # X = sparse_random_matrix(100, 100, density=0.01, random_state=42)
#
# svd = TruncatedSVD(n_components=5)
#
# X_reduced = svd.fit_transform(X)
#



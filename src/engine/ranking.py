from __future__ import print_function

import numpy as np
import psycopg2
from collections import Counter

from preprocess import preprocess_body, preprocess_body_lda
from queries import get_dictionary_size, get_all_documents, get_tf_idf_scores, get_document_by_id
from model_funcs.similarities import dot_product

conn = psycopg2.connect(database='reuters', user='mkurnikov', password='vfrcbv')
cursor = conn.cursor()

def count_ranking(query):
    # print query
    query_words = preprocess_body(query).split(' ')
    # print query_words
    # = np.zeros((get_dictionary_size(cursor)))
    query_word_counter = Counter()
    # print query_words
    for word in query_words:
        query_word_counter[word] += 1

    import time
    before = time.time()
    all_docs = get_all_documents(cursor)
    # queries_time = time.time()
    # zero_time = time.time()
    # print queries_time
    similarities = []
    for i, doc_id in enumerate(all_docs):
        # b = time.time()
        document_tf_idf_scores = get_tf_idf_scores(cursor, doc_id)
        # queries_time += (time.time() - b)
        # query_tf_scores = np.zeros((len(document_tf_idf_scores)), dtype=np.float32)
        query_tf = np.zeros((len(document_tf_idf_scores)))
        # print query_word_counter.keys()
        for j, row in enumerate(document_tf_idf_scores):
            word, tf_idf = row
            # print word
            if word in query_word_counter:
                query_tf[j] = query_word_counter[word]
            # print query_tf
        if i % 1000 == 0:
            print('processed:', i, 'time:', time.time() - before)

        document_tf_idf_presentation = [tf_idf for word, tf_idf in document_tf_idf_scores]
        try:
            similarities.append((doc_id, dot_product(query_tf, document_tf_idf_presentation)))
        except TypeError:
            import debug
    top = sorted(similarities, key=lambda x: x[1], reverse=True)
    return top

import pickle
import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.metrics.pairwise import cosine_similarity

def lsi_ranking(query):
    documents = pickle.load(open(settings.DOCUMENTS_LSI))
    vectorizer = pickle.load(open(settings.VECTORIZER_LSI))
    lsa = pickle.load(open(settings.LSI_MODEL))

    query = vectorizer.transform([preprocess_body(query)])
    query = lsa.transform(query)
    query = Normalizer().fit_transform(query)

    sim = cosine_similarity(query, documents)
    sorted_indices = np.argsort(sim)
    sim = sim[:, sorted_indices.flatten()]
    tuples = np.concatenate((sorted_indices, sim), axis=0)
    return tuples.T[::-1]


from gensim import corpora, models, similarities
def lda_ranking(query):
    dictionary = corpora.Dictionary.load(settings.DICTIONARY)
    query = preprocess_body_lda(query).split(' ')
    query_corpus = [dictionary.doc2bow(query)]

    tfidf_model = models.TfidfModel.load(settings.TF_IDF_MODEL)
    logentropy_model = models.LogEntropyModel.load(settings.LOGENTROPY_MODEL)
    lda_model = models.LdaModel.load(settings.LDA_MODEL)
    similarity_matrix = similarities.MatrixSimilarity.load(settings.SIMILARITY_MATRIX)

    query_similarities = similarity_matrix.get_similarities(lda_model[query_corpus])
    sorted_indices = query_similarities.argsort()
    sim = query_similarities[:, sorted_indices.flatten()]

    tuples = np.concatenate((sorted_indices, sim), axis=0)
    return tuples.T[::-1]







if __name__ == '__main__':
    import time
    before = time.time()
    print(lda_ranking('dog ate a cat'))

    print('time:', time.time() - before)




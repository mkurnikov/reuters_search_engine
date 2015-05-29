from __future__ import division
import math

def tf_idf_model(tf, df, n_documents):
    return tf * math.log((n_documents + 1) / df)

def bm25(tf, df, n_documents, k=1):
    return (k + 1) * tf / (tf + k) * math.log((n_documents + 1) / df)

# def pivot_normalization(tf, df, n_documents)
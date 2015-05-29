import numpy as np

def dot_product(query_tf_idf_scores, document_tf_idf_scores):
    query_bag = np.array(query_tf_idf_scores)
    document_bag = np.array(document_tf_idf_scores)
    if document_tf_idf_scores is None or len(document_tf_idf_scores) == 0:
        # print query_bag
        print document_bag
        # print ''
    if query_tf_idf_scores is None or len(query_tf_idf_scores) == 0:
        # print query_bag
        print query_bag
        # print ''
    return (query_bag * document_bag).sum()

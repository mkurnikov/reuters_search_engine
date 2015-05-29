import psycopg2

from queries import get_words_doc_pairs_with_tf_and_df, add_tf_idf_score
from model_funcs.scores import tf_idf_model, bm25

conn = psycopg2.connect(database='reuters', user='mkurnikov', password='vfrcbv')
cursor = conn.cursor()
N_DOCUMENTS = 21578

import time
before = time.time()
i = 1
for word, doc_id, tf, df in get_words_doc_pairs_with_tf_and_df(cursor):
    # add_tf_idf_score(cursor, word, doc_id, tf_idf_model(tf, df, N_DOCUMENTS))
    add_tf_idf_score(cursor, word, doc_id, bm25(tf, df, N_DOCUMENTS))

    if i % 1000 == 0:
        conn.commit()
    i += 1

    if i % 20000 == 0:
        print 'processed %dk' % int(i / 1000), 'time:', time.time() - before
conn.commit()
conn.close()

print 'overall time:', time.time() - before


def insert_document(cursor, title, body, doc_length, topics):
    cursor.execute('INSERT INTO documents(title_raw, body_raw, doc_length, topics) VALUES (%s, %s, %s, %s) RETURNING document_id;',
                   (title, body, doc_length, topics))
    return cursor.fetchone()


def append_word_documents_frequency(cursor, word, df):
    cursor.execute('UPDATE dictionary '
                   'SET document_frequency=document_frequency+%s '
                   'WHERE word=%s', (df, word))
    if cursor.rowcount == 0:
        cursor.execute('INSERT INTO dictionary(word, document_frequency) '
                       'VALUES (%s, %s)', (word, df))


def add_record_to_inv_index(cursor, word, doc_id, tf):
    cursor.execute('INSERT INTO inverted_index(word, document_id, term_frequency) '
                   'VALUES (%s, %s, %s)',
                   (word, doc_id, tf))


def add_tf_idf_score(cursor, word, doc_id, tf_idf_score):
    cursor.execute('UPDATE inverted_index SET tf_idf_score=%s WHERE word=%s AND document_id=%s', (tf_idf_score, word, doc_id))


def get_words_doc_pairs_with_tf_and_df(cursor):
    # if batch_size != -1:
    #     cursor.execute('SELECT term_frequency, document_frequency '
    #                    'FROM dictionary JOIN inverted_index ON (dictionary.word=inverted_index.word)'
    #                    'WHERE tf_idf_score IS NOT NULL '
    #                    'LIMIT %s', (batch_size))
    #     return cursor.fetchall()
    # else:
    cursor.execute('SELECT dictionary.word, document_id, term_frequency, document_frequency '
                           'FROM dictionary JOIN inverted_index ON (dictionary.word=inverted_index.word)'
                           'WHERE tf_idf_score IS NULL')
    return cursor.fetchall()


def get_all_words(cursor, batch_size=-1):
    if batch_size != -1:
        cursor.execute('SELECT word FROM dictionary; ')


def get_dictionary_size(cursor):
    cursor.execute('SELECT COUNT(*) FROM dictionary;')
    return cursor.fetchone()


def get_tf_idf_scores(cursor, doc_id):
    cursor.execute('SELECT word, tf_idf_score FROM inverted_index WHERE document_id=%s;' % (doc_id))
    return cursor.fetchall()


def get_all_documents(cursor):
    cursor.execute('SELECT document_id FROM documents')
    return cursor.fetchall()

def get_document_by_id(cursor, doc_id):
    cursor.execute('SELECT title_raw, body_raw, topics FROM documents WHERE document_id=%s' % (doc_id))
    return cursor.fetchone()
#
# def get_dictionary(cursor):
#     cursor.execute('SELECT word FROM dictionary')
#     return cursor.fetchall()



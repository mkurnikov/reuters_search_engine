from __future__ import print_function

import psycopg2
from collections import Counter

from queries import insert_document, append_word_documents_frequency, add_record_to_inv_index
from preprocess import preprocess_body
from parsers.reuters import ReutersParser

conn = psycopg2.connect(database='reuters', user='mkurnikov', password='vfrcbv')
cursor = conn.cursor()

DATA_FOLDER = '/home/mkurnikov/_python/reuters/data/'

import time
before = time.time()

parser = ReutersParser(DATA_FOLDER)
for i, article in enumerate(parser.parse()):
    if (i % 1000 == 0):
        print('document parsed:', i, 'time:', time.time() - before)
    body_prepared = preprocess_body(article['body'])
    doc_id = insert_document(cursor, article['title'], article['body'], len(body_prepared.split(' ')), article['topics'])

    word_counter = Counter()
    for word in body_prepared.split(' '):
        word_counter[word] += 1

    for word, counter in word_counter.items():
        append_word_documents_frequency(cursor, word, counter)
        add_record_to_inv_index(cursor, word, doc_id, counter)
    if i % 10 == 0:
        conn.commit()
conn.commit()
conn.close()

print('overall time:', time.time() - before)
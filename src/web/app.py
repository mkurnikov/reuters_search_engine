from flask import Flask, g, render_template, request, redirect
import psycopg2

import sys
sys.path.append('/home/mkurnikov/_python/reuters')
from src.engine.queries import get_document_by_id
from src.engine.ranking import count_ranking, lsi_ranking, lda_ranking

DATABASE = 'reuters'
USERNAME = 'mkurnikov'
PASSWORD = 'vfrcbv'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return psycopg2.connect(database=app.config['DATABASE'], user=app.config['USERNAME'], password=app.config['PASSWORD'])

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def search_page():
    # return 'Hello, world'
    return render_template('search.html', articles=[])


@app.route('/query', methods=['GET'])
def find_documents():
    # return redirect('/')
    articles = []
    db = getattr(g, 'db', None)
    if db is not None:
        cursor = db.cursor()
        query = request.args['query']
        top = count_ranking(query)[:10]
        for doc_id, sim in top:
            title_raw, body_raw, topics = get_document_by_id(cursor, doc_id)
            articles.append({'title': title_raw, 'body': body_raw, 'similarity': sim, 'topics': topics})
    # articles = [{'title': 'Article1', 'body': 'Some text'}, {'title': 'Article2', 'body': 'Some text'}]
    return render_template('search.html', articles=articles)


@app.route('/lsi', methods=['GET'])
def find_documents_lsi():
    # query = request.args['query']
    articles = []
    db = getattr(g, 'db', None)
    if db is not None:
        cursor = db.cursor()
        query = request.args['query']
        top = lsi_ranking(query)[:10]
        # print(top)
        # import sys; sys.exit(1)
        for doc_id, sim in top:
            title_raw, body_raw, topics = get_document_by_id(cursor, doc_id)
            articles.append({'title': title_raw, 'body': body_raw, 'similarity': sim, 'topics': topics})
    # articles = [{'title': 'Article1', 'body': 'Some text'}, {'title': 'Article2', 'body': 'Some text'}]
    return render_template('search.html', articles=articles)


@app.route('/lda', methods=['GET'])
def find_documents_lda():
    # query = request.args['query']
    articles = []
    db = getattr(g, 'db', None)
    if db is not None:
        cursor = db.cursor()
        query = request.args['query']
        top = lda_ranking(query)[:10]
        # print(top)
        # import sys; sys.exit(1)
        for doc_id, sim in top:
            title_raw, body_raw, topics = get_document_by_id(cursor, doc_id)
            articles.append({'title': title_raw, 'body': body_raw, 'similarity': sim, 'topics': topics})
    # articles = [{'title': 'Article1', 'body': 'Some text'}, {'title': 'Article2', 'body': 'Some text'}]
    return render_template('search.html', articles=articles)



if __name__ == '__main__':
    app.run()





















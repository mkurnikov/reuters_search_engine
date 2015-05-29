import os

PROJECT_ROOT = os.path.dirname(__file__)

DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data/')

N_DOCUMENTS = 21578

### For LDA
DOCUMENTS_LIST_PKL = os.path.join(PROJECT_ROOT, 'data/documents.pkl')

DICTIONARY = os.path.join(PROJECT_ROOT, 'data/reuters.dict')

CORPUS = os.path.join(PROJECT_ROOT, 'data/corpus.mm')

LDA_MODEL = os.path.join(PROJECT_ROOT, 'data/lda.model')

TF_IDF_MODEL = os.path.join(PROJECT_ROOT, 'data/tfidf.model')

LOGENTROPY_MODEL = os.path.join(PROJECT_ROOT, 'data/logentropy.model')

SIMILARITY_MATRIX = os.path.join(PROJECT_ROOT, 'data/sim.matrix')

### For LSI-based search
LSI_MODEL = os.path.join(PROJECT_ROOT, 'data/lsi.model')

DOCUMENTS_LSI = os.path.join(PROJECT_ROOT, 'data/documents-lsi.pkl')

VECTORIZER_LSI = os.path.join(PROJECT_ROOT, 'data/vectorizer-lsi.pkl')
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
english_stopwords = set(stopwords.words('english'))
#
# def _preprocess_text(text):
#     text = text.strip().lower()
#     # text = re.sub(r'[^A-Za-z-]', ' ', text)
#     meaningful_words = [w for w in re.findall(r'[a-zA-Z]+[-]*[a-zA-Z]+', text) if w not in english_stopwords]
#     return " ".join(meaningful_words)

def preprocess_title(title):
    return title.strip().lower()

stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()
def preprocess_body(body):
    # initial preprocessing(lower case, strip spaces
    body = body.strip().lower()
    # find only words match specified regex
    words = re.findall(r'[a-zA-Z]+[-]*[a-zA-Z]+', body)
    # stem all words with nltk.stem.PorterStemmer
    stemmed_words = [lemmatizer.lemmatize(word) for word in words]
    # stemmed_words = [stemmer.stem(word) for word in words]
    # remove stops
    without_stops = [word for word in stemmed_words
                     if word not in english_stopwords]

    return " ".join(without_stops)

vowels = {'a', 'o', 'u', 'e', 'i'}
skipped_words = {'blah', 'said', 'would', 'reuter'}
def preprocess_body_lda(body):
    doc = preprocess_body(body).split(" ")
    new_doc = []
    for word in doc:
        if any([vowel in word for vowel in vowels]) and word not in skipped_words and len(word) > 2:
            new_doc.append(word)
    return " ".join(new_doc)



def preprocess_article(article):
    article['title'] = preprocess_title(article['title'])
    article['body'] = preprocess_body(article['body'])
    return article
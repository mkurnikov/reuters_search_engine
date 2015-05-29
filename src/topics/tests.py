import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pickle
import settings

from gensim import corpora, models
lsi = models.LdaModel.load(settings.LDA_MODEL)
topics = lsi.show_topics(num_topics=30, num_words=5, formatted=False)
print topics
#
# for topic in topics:
#     sorted_topic = sorted(topic, key=lambda x: x[0], reverse=True)
#     print " ".join([prob_word_pair for prob_word_pair in sorted_topic])
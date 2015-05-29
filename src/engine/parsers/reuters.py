from bs4 import BeautifulSoup
import os

class ReutersParser(object):
    def __init__(self, DATA_FOLDER):
        self.DATA_FOLDER = DATA_FOLDER

    def parse(self):
        for fname in os.listdir(self.DATA_FOLDER):
            if os.path.splitext(fname)[-1] == '.sgm':
                # parse file - want to add nested generator but dunno how
                with open(os.path.join(self.DATA_FOLDER, fname)) as f:
                    documents = BeautifulSoup(f.read())
                    for article_node in documents.find_all('reuters'):
                        yield self._parse_node(article_node)


    def _parse_node(self, node):
        article = {}

        text_node = node.find('text')
        dateline_node = text_node.find('dateline')
        if dateline_node:
            dateline_node.extract()
        title_node = text_node.find('title')
        article['title'] = title_node.extract().get_text() if title_node else ''
        article['body'] = text_node.get_text()

        article['topics'] = [topic_node.get_text() for topic_node in node.find('topics').find_all('d')] \
                                                if node['topics'] == 'YES' else []
        return article
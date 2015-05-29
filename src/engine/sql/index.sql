CREATE INDEX tf_idf_index ON inverted_index (tf_idf_score);
CREATE INDEX word_index ON inverted_index(word);
CREATE INDEX doc_id_index ON inverted_index(document_id);
DROP INDEX IF EXISTS tf_idf_index;
DROP INDEX IF EXISTS word_index;
DROP INDEX IF EXISTS doc_id_index;

DROP TABLE IF EXISTS inverted_index;
DROP TABLE IF EXISTS dictionary;
DROP TABLE IF EXISTS documents;

CREATE TABLE dictionary (
  word VARCHAR NOT NULL PRIMARY KEY ,
  document_frequency INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE documents (
  document_id SERIAL NOT NULL PRIMARY KEY ,
  title_raw VARCHAR NOT NULL ,
  body_raw TEXT NOT NULL ,
  topics TEXT[],
  doc_length INTEGER NOT NULL
);

CREATE TABLE inverted_index (
  word VARCHAR REFERENCES dictionary(word),
  document_id INTEGER REFERENCES documents(document_id),
  term_frequency INTEGER NOT NULL DEFAULT 1,
  tf_idf_score FLOAT,
  PRIMARY KEY (word, document_id)
);
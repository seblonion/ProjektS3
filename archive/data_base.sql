CREATE DATABASE Learning;
USE Learning;

CREATE TABLE Langues (
    langue_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE Topics(
	topic_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    nom TEXT,
    langue_id INTEGER NOT NULL,
    FOREIGN KEY (langue_id) REFERENCES Langues(langue_id)
);

CREATE TABLE Sentences (
    sentence_id INTEGER AUTO_INCREMENT PRIMARY KEY,
	content TEXT,
    bonne_reponse TEXT
);


CREATE TABLE Exercises (
    exercice_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    nom TEXT,
    niveau INTEGER,
    topic_id INTEGER,
	CONSTRAINT unique_niveau_topic UNIQUE (niveau, topic_id),
    sentence_id INTEGER,
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id),
    FOREIGN KEY (sentence_id) REFERENCES Sentences(sentence_id)
);


CREATE TABLE Cours(
	cours_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    topic_id INTEGER,
    FOREIGN KEY (topic_id) REFERENCES Topics(topic_id)
);












CREATE TABLE IF NOT EXISTS Languages
(
    uid  INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS Topics
(
    uid         INTEGER PRIMARY KEY AUTOINCREMENT,
    nom         TEXT,
    language_id INTEGER NOT NULL,
    FOREIGN KEY (language_id) REFERENCES Languages (uid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Exercises
(
    uid       INTEGER PRIMARY KEY AUTOINCREMENT,
    nom       TEXT,
    level     INTEGER,
    topic_id  INTEGER,
    is_solved INTEGER DEFAULT 0,
    CONSTRAINT unique_level_topic UNIQUE (level, topic_id),
    FOREIGN KEY (topic_id) REFERENCES Topics (uid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Sentences
(
    uid         INTEGER PRIMARY KEY AUTOINCREMENT,
    content     TEXT,
    answer      TEXT,
    exercise_id INTEGER REFERENCES Exercises (uid) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS Lessons
(
    uid      INTEGER PRIMARY KEY AUTOINCREMENT,
    content  TEXT,
    topic_id INTEGER,
    FOREIGN KEY (topic_id) REFERENCES Topics (uid) ON DELETE CASCADE
);












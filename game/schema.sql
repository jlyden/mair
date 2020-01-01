DROP TABLE IF EXISTS owl;
DROP TABLE IF EXISTS world;

CREATE TABLE owl (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL, 
    life INTEGER NOT NULL,
    mice INTEGER NOT NULL
);

CREATE TABLE world (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owl_id INTEGER NOT NULL,
    day INTEGER NOT NULL,
    nightfall BOOLEAN NOT NULL,
    mouse_pop INTEGER NOT NULL,
    FOREIGN KEY (owl_id) REFERENCES owl (id)
);
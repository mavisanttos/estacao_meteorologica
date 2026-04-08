DROP TABLE IF EXISTS leituras;

CREATE TABLE leituras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL NOT NULL,
    umidade REAL NOT NULL,
    sensacao REAL NOT NULL,
    timestamp DATETIME DEFAULT (datetime('now','localtime'))
);
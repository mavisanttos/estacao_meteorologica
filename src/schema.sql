CREATE TABLE IF NOT EXISTS leituras ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL NOT NULL, 
    umidade REAL NOT NULL,
    pressao REAL,
    sensacao_termica REAL,
    previsao TEXT,
    timestamp DATETIME DEFAULT (datetime('now','localtime')),
    unix_timestamp INTEGER
);
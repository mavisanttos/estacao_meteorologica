import sqlite3
import os

DB_NAME = 'dados.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, timeout=20)
    
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        with open('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
    print("Banco de dados inicializado com sucesso!")

def inserir_leitura(temperatura, umidade, sensacao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leituras (temperatura, umidade, sensacao)
        VALUES (?, ?, ?)
    ''', (temperatura, umidade, sensacao))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

def listar_leituras(limite=50):
    conn = get_db_connection()
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?', (limite,)).fetchall()
    conn.close()
    return [dict(ix) for ix in leituras]

def buscar_leitura(id):
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id,)).fetchone()
    conn.close()
    return leitura

def atualizar_leitura(id, temperatura, umidade, sensacao):
    conn = get_db_connection()
    conn.execute('''
        UPDATE leituras 
        SET temperatura = ?, umidade = ?, sensacao = ?
        WHERE id = ?
    ''', (temperatura, umidade, sensacao, id))
    conn.commit()
    conn.close()

def deletar_leitura(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
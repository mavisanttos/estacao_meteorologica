import sqlite3
import time

def get_db_connection():
    conn = sqlite3.connect('dados.db', timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def inserir_leitura(temp, umid, press, sensacao, prev):
    conn = get_db_connection()
    cursor = conn.cursor()
    unix_now = int(time.time())
    
    cursor.execute('''
        INSERT INTO leituras (temperatura, umidade, pressao, sensacao_termica, previsao, unix_timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (temp, umid, press, sensacao, prev, unix_now))
    
    id_gerado = cursor.lastrowid
    conn.commit()
    conn.close()
    return id_gerado

def listar_leituras(limite=50):
    conn = get_db_connection()
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?', (limite,)).fetchall()
    conn.close()
    return leituras

def buscar_leitura(id):
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id,)).fetchone()
    conn.close()
    return leitura

def atualizar_leitura(id, dados):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE leituras 
        SET temperatura = ?, umidade = ?, pressao = ?, sensacao_termica = ?, previsao = ?
        WHERE id = ?
    ''', (dados['temperatura'], dados['umidade'], dados.get('pressao'), 
          dados.get('sensacao_termica'), dados.get('previsao'), id))
    
    linhas_alteradas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas_alteradas > 0

def deletar_leitura(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM leituras WHERE id = ?', (id,))
    linhas_deletadas = cursor.rowcount
    conn.commit()
    conn.close()
    return linhas_deletadas > 0
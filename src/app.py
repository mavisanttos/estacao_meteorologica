from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (get_db_connection, inserir_leitura, listar_leituras, 
                      deletar_leitura, buscar_leitura, atualizar_leitura)
import os
from config import DEBUG_MODE

app = Flask(__name__)

@app.route('/')
def index():
    dados = listar_leituras(limite=10)
    return render_template('index.html', leituras=dados)

@app.route('/leituras', methods=['GET'])
def listar():
    dados = listar_leituras(limite=50)
    if request.args.get('formato') == 'json':
        return jsonify(dados)
    return render_template('historico.html', leituras=dados)

@app.route('/leituras', methods=['POST'])
def criar_leitura():
    dados = request.get_json()
    if not dados: 
        return jsonify({'erro': 'Sem dados'}), 400

    temp = dados.get('temperatura')
    umid = dados.get('umidade')
    sens = dados.get('sensacao', 0)
    
    if temp is None or umid is None:
        return jsonify({'erro': 'Temperatura ou Umidade ausentes'}), 400

    inserir_leitura(temp, umid, sens)
    return jsonify({'status': 'sucesso'}), 201

@app.route('/leituras/<int:id>', methods=['GET'])
def detalhe(id):
    leitura = buscar_leitura(id)
    if not leitura:
        return jsonify({'erro': 'Não encontrado'}), 404
    
    if request.args.get('formato') == 'json':
        return jsonify(dict(leitura))
    return render_template('editar.html', leitura=leitura)

@app.route('/leituras/<int:id>', methods=['POST', 'PUT'])
def atualizar(id):
    if request.method == 'PUT' or request.is_json:
        dados = request.get_json()
        temp = dados.get('temperatura')
        umid = dados.get('umidade')
        sens = dados.get('sensacao')
    else:
        temp = request.form.get('temperatura')
        umid = request.form.get('umidade')
        sens = request.form.get('sensacao')
    
    atualizar_leitura(id, temp, umid, sens)
    
    if request.method == 'PUT':
        return jsonify({'status': 'atualizado'}), 200
    return redirect(url_for('listar'))

@app.route('/leituras/deletar/<int:id>', methods=['POST', 'DELETE'])
def deletar(id):
    deletar_leitura(id)
    if request.method == 'DELETE':
        return jsonify({'status': 'removido'}), 200
    return redirect(url_for('listar'))

@app.route('/medir', methods=['POST'])
def solicitar_medicao():
    try:
        with open('comando.txt', 'w') as f:
            f.write('LER')
        return jsonify({'status': 'Solicitação enviada'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/estatisticas')
def estatisticas():
    try:
        conn = get_db_connection()
        stats = conn.execute('SELECT AVG(temperatura), MAX(temperatura), MIN(temperatura) FROM leituras').fetchone()
        conn.close()
        return jsonify({
            'media': round(stats[0], 2) if stats[0] else 0, 
            'max': stats[1] if stats[1] else 0, 
            'min': stats[2] if stats[2] else 0
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/editar/<int:id>')
def editar_pagina(id):
    leitura = buscar_leitura(id)
    if not leitura:
        return "Leitura não encontrada", 404
    return render_template('editar.html', leitura=leitura)

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, port=5000)
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import inserir_leitura, listar_leituras, buscar_leitura, atualizar_leitura, deletar_leitura, init_db

app = Flask(__name__)

def calcular_sensacao(temp, umid):
    return round(temp + 0.05 * umid, 2)

def calcular_previsao(pressao):
    if pressao is None:
        return "N/A"
    if pressao < 1000:
        return "Chuva / Tempestade"
    elif 1000 <= pressao < 1015:
        return "Instável"
    else:
        return "Tempo Bom / Seco"

@app.route('/')
def index():
    dados = listar_leituras(limite=10)
    return render_template('index.html', leituras=dados)

@app.route('/leituras', methods=['GET', 'POST'])
def leituras():
    if request.method == 'POST':
        dados_json = request.get_json()
        
        temp = dados_json.get('temperatura')
        umid = dados_json.get('umidade')
        press = dados_json.get('pressao')
        sensacao = calcular_sensacao(temp, umid)
        previsao = calcular_previsao(press)
        
        id_novo = inserir_leitura(temp, umid, press, sensacao, previsao)
        return jsonify({"status": "sucesso", "id": id_novo}), 201

    formato = request.args.get('formato')
    dados = listar_leituras(limite=100)
    
    if formato == 'json':
        return jsonify([dict(row) for row in dados])
    
    return render_template('historico.html', leituras=dados)

@app.route('/leituras/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def detalhe_leitura(id):
    if request.method == 'GET':
        leitura = buscar_leitura(id)
        if not leitura:
            return "Não encontrado", 404
        return render_template('editar.html', leitura=leitura)

    if request.method == 'DELETE':
        sucesso = deletar_leitura(id)
        return jsonify({"sucesso": sucesso})

    if request.method == 'PUT':
        dados_novos = request.get_json()
        sucesso = atualizar_leitura(id, dados_novos)
        return jsonify({"sucesso": sucesso})

@app.route('/api/estatisticas')
def estatisticas():
    return jsonify({"mensagem": "Em implementação para o Chart.js"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
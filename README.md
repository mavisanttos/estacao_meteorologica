# Estação Meteorológica - Maria Vitória dos Santos

&emsp; Esta documentação reflete o desenvolvimento completo de uma simulação de um monitor climático que integra hardware a uma infraestrutura de software baseada em microserviços e APIs REST. A aplicação permite a coleta, persistência, visualização e edição de dados meteorológicos em tempo real.

## Funcionalidades Principais

- **Coleta On-Demand (Trigger):**  
  Diferente de sensores passivos, esta estação só realiza leituras quando solicitada pelo Dashboard (Botão "Medir Agora").

- **Dashboard Interativo:**  
  Gráficos dinâmicos gerados com Chart.js comparando Temperatura e Umidade.

- **Cálculo de Sensação Térmica:**  
  O backend processa o Índice de Calor (Heat Index) para uma medição mais precisa do conforto humano.

- **Feedback Visual via Hardware:**  
  Um LED RGB conectado ao Arduino muda de cor instantaneamente com base na sensação térmica calculada.

- **CRUD Completo:**  
  Gestão total das medições através de uma interface web (Criar, Listar, Editar e Excluir).

- **Exportação de Dados:**  
  Suporte nativo para exportação de leituras em formato JSON via API.


## Arquitetura e Estrutura de Arquivos

O projeto está dividido em camadas para facilitar a manutenção:

```plaintext
├── arduino/
│   └── estacao.ino        # Lógica C++ (Leitura DHT11 e Controle LED RGB)
├── static/
│   ├── css/style.css      # Estilização visual (Bootstrap Custom)
│   └── js/main.js         # Lógica do Gráfico e requisições AJAX
├── templates/
│   ├── base.html          # Template mestre e navegação
│   ├── index.html         # Dashboard e Gráfico
│   ├── historico.html     # Listagem completa e deleção
│   └── editar.html        # Formulário de edição de registros
├── app.py                 # Servidor Flask (API REST principal)
├── database.py            # Camada de abstração do Banco de Dados
├── serial_reader.py       # Script de ponte (Serial <-> API)
├── config.py              # Centralização de portas e configurações
├── schema.sql             # Definição das tabelas do banco
└── dados.db               # Banco de dados SQLite (com +30 leituras)
```

## Endpoints

A API responde tanto em HTML quanto em JSON, usando o parâmetro `?formato=json`.

| Método | Rota                          | Função        | Descrição                                                  |
|--------|-------------------------------|--------------|------------------------------------------------------------|
| GET    | /                             | index()      | Painel principal com as últimas 10 leituras e gráfico       |
| GET    | /leituras                     | listar()     | Histórico completo                                         |
| POST   | /leituras                     | criar()      | Recebe dados do Arduino via Serial Reader                  |
| GET    | /leituras/<id>                | detalhe()    | Exibe/Retorna uma leitura específica por ID                |
| PUT/POST | /leituras/<id>              | atualizar()  | Atualiza os dados de uma leitura existente                 |
| DELETE/POST | /leituras/deletar/<id>  | deletar()    | Remove permanentemente um registro do banco                |
| GET    | /api/estatisticas             | estatisticas() | Retorna Média, Máxima e Mínima em JSON                  |
| POST   | /medir                        | solicitar()  | Envia o sinal de trigger para o Arduino                    |

## Front-end

A interface foi construída utilizando **Bootstrap 5**, focando em responsividade e clareza visual.

### Dashboard (Index)
- Indicador de Status: Notificações em tempo real sobre o sucesso ou erro das medições  
- Gráfico Temporal: Linhas suaves que mostram a variação climática recente  

**Status de Conforto térmico:**
- Azul (Frio): < 20°C  
- Verde (Ideal): 20°C - 27°C  
- Vermelho (Quente): > 27°C  

*obs: essas cores também podem ser visualizadas no LED RGD do hardware*

### Histórico
- Tabela administrativa completa  
- Formatação de data/hora local  
- Exclusão de registros  

### Edição
- Formulário intuitivo  
- Validação de campos  
- Correção de dados manuais  

##  Instruções de Instalação e Execução

### 1. Requisitos
- Python 3.x instalado  
- Arduino com sensor DHT11 e LED RGB  
  - Pins: R=9, G=10, B=11  

### 2. Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/mavisanttos/estacao_meteorologica.git
code .
cd src
```

Crie e ative uma venv:

```bash
# para windows:
python -m venv venv
venv\Scripts\activate

# para mac/linux:
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Configuração

Edite o arquivo `config.py` para definir a porta correta:

```python
SERIAL_PORT = 'COM12'  # define a porta de conexão com o hardware
```

### 4. Execução (dois terminais)

**Terminal 1 (Backend):**
```bash
python app.py
```

**Terminal 2 (Ponte Serial):**
```bash
python serial_reader.py
```

Acesse no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Boas Práticas Implementadas

- **Modo WAL no SQLite:** Permite leitura e escrita simultânea sem travamentos  
- **Tratamento de Erros:** Detecta automaticamente desconexão do Arduino  
- **Configurações Centralizadas:** Uso de `config.py` para portabilidade  
- **Segurança no Trigger:** Uso de arquivo intermediário (`comando.txt`)  

---

## Demonstração em Vídeo

&emsp; Veja o funcionamento do projeto: [Vídeo](https://youtu.be/7MT9QdJhaPM?si=UrSc3_Hn-TMFJ8U4)  

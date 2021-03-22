from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for, abort
from flask_httpauth import HTTPBasicAuth
import datetime
import random

auth = HTTPBasicAuth()
app = Flask(__name__)
tempoRecebido = []

@app.route('/relogio', methods=['GET'])
def obter_relogio():
    return jsonify({'tempoRecebido': tempoRecebido})

@app.route('/enviarrelogio', methods=['GET'])
def att_relogio():
    r = random.randrange(5, 30) #tempo aleatório pra ser alterado
    current_time = datetime.datetime.now() #tempo atual
    format_hour = current_time.hour #hora
    format_minute =current_time.minute #minuto
    format_seconds = current_time.second #segundo
    secondstominutes = format_seconds + r
    if(secondstominutes >= 60): # covertendo segundos para minutos pra tirar a diferença que sobrou
        format_seconds = secondstominutes - 60 # tirando 60 segundos (minuto)
        if (format_minute > 59):
            format_minute = 0
            format_hour = format_hour + 1
        else:    
            format_minute = format_minute + 1 # colocando o minuto 
    else:    
        format_seconds = format_seconds + r
    format_hour = "{:02d}".format(format_hour)
    format_minute = "{:02d}".format(format_minute)
    format_seconds = "{:02d}".format(format_seconds)
    params ={
        'nome': 'T2',
        'hora': format_hour,
        'minuto': format_minute,
        'segundo': format_seconds
    }
    tempoRecebido.append(params)
    return jsonify({'tempoRecebido': tempoRecebido})

@app.route('/relogio', methods=['POST'])
def receber_hora():
    if not request.json or not 'nome' in request.json:
        abort(400)
    tempo = {
        'nome': request.json['nome'],
        'hora': request.json.get('hora', ""),
        'minuto': request.json.get('minuto', ""),
        'segundo': request.json.get('segundo', "")
    }
    tempoRecebido.append(tempo)
    current_time = datetime.datetime.now()
    format_hour = "{:02d}".format(current_time.hour)
    format_minute = "{:02d}".format(current_time.minute)
    format_seconds = "{:02d}".format(current_time.second)
    tempoSistema = {
        'nome': 'T1',
        'hora': format_hour,
        'minuto': format_minute,
        'segundo': format_seconds
    }
    tempoRecebido.append(tempoSistema)
    return jsonify({'tempo': tempo}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)

if __name__ == "__main__":
    print('Servidor executando...')
    app.run(debug=True)
import random
from datetime import datetime, timedelta
import requests
import time

def main():
    r = random.randrange(5, 30) #tempo aleatório pra ser alterado
    current_time = datetime.now() #tempo atual
    format_hour = current_time.hour #hora
    format_minute =current_time.minute #minuto
    format_seconds = current_time.second #segundo
    secondstominutes = format_seconds - r
    if(secondstominutes < 0): # covertendo minutos para segundos pra tirar a diferença que sobrou
        if (format_minute == 0):
            if (format_hour == 0):
                format_hour = 23
                format_minute = 59
                format_seconds = 0
            else:
                format_hour = format_hour - 1
                format_minute = 59
                format_seconds = 0    
        else:    
            format_minute = format_minute -1 # diminuindo 1 minuto.
            format_seconds = 60 + secondstominutes # transferindo pra cá e tirando a diferença.
    else:    
        format_seconds = format_seconds - r
    format_hour = "{:02d}".format(format_hour)
    format_minute = "{:02d}".format(format_minute)
    format_seconds = "{:02d}".format(format_seconds)
    params ={
        'nome': 'T0',
        'hora': format_hour,
        'minuto': format_minute,
        'segundo': format_seconds
    }
    requests.post('http://127.0.0.1:5000/relogio', json=params)

    # calculo e defasagem
    r = requests.get("http://127.0.0.1:5000/enviarrelogio")
    data = r.json()
    print(data)
    for i in range(len(data['tempoRecebido'])):
        if (data['tempoRecebido'][i]['nome'] == "T0"):
            horaT0 = data['tempoRecebido'][i]['hora']
            minutoT0 = data['tempoRecebido'][i]['minuto']
            segundoT0 = data['tempoRecebido'][i]['segundo']
            T0 = timedelta(hours = int(horaT0), minutes = int(minutoT0), seconds = int(segundoT0), microseconds=0)
        elif (data['tempoRecebido'][i]['nome'] == "T1"):
            horaT1 = data['tempoRecebido'][i]['hora']
            minutoT1 = data['tempoRecebido'][i]['minuto']
            segundoT1 = data['tempoRecebido'][i]['segundo']
            T1 = timedelta(hours = int(horaT1), minutes = int(minutoT1), seconds = int(segundoT1), microseconds=0)
        elif (data['tempoRecebido'][i]['nome'] == "T2"):
            horaT2 = data['tempoRecebido'][i]['hora']
            minutoT2 = data['tempoRecebido'][i]['minuto']
            segundoT2 = data['tempoRecebido'][i]['segundo']
            T2 = timedelta(hours = int(horaT2), minutes = int(minutoT2), seconds = int(segundoT2), microseconds=0)

    lado1 = T1 - T0
    print("HORA T0 ->", T0)
    print("HORA T1 ->", T1)
    print("Primeiro Lado ->", lado1)

    T3 = T0 + timedelta(seconds = 3)
    lado2 = T2 - T3
    print("HORA T2 ->", T2)
    print("HORA T3 ->", T3)
    print("Segundo Lado ->", lado2)

    defasagem = (lado1 + lado2)//2
    print("Defasagem:", defasagem)

    T4 = timedelta(hours = current_time.hour, minutes = current_time.minute, seconds = current_time.second, microseconds=0)
    print("Tempo Atual:", T4)
    T4 = T4 + defasagem
    print("Tempo Atual + Defasagem:", T4)

if __name__ == "__main__":
    main()
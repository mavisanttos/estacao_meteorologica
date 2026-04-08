import serial
import json
import requests
import time
import os
from config import SERIAL_PORT, BAUD_RATE, API_URL

PORTA = SERIAL_PORT
BAUD = BAUD_RATE
URL_API = API_URL
COMANDO_FILE = 'comando.txt'

def ler_serial():
    print(f"Monitorando porta {PORTA} e arquivo {COMANDO_FILE}...")
    try:
        ser = serial.Serial(PORTA, BAUD, timeout=0.1)
    except serial.SerialException as e:
        print(f"ERRO: Não foi possível abrir a porta {PORTA}. O Arduino está conectado?")
        exit()

        while True:
            if os.path.exists(COMANDO_FILE):
                ser.write(b'L') 
                os.remove(COMANDO_FILE)
                print("Comando 'L' enviado ao Arduino!")

            if ser.in_waiting > 0:
                linha = ser.readline().decode('utf-8').strip()
                if linha.startswith('{'):
                    try:
                        dados = json.loads(linha)
                        requests.post(URL_API, json=dados)
                        print(f"Dados salvos: {dados}")
                    except:
                        print(f"Erro ao processar: {linha}")
            
            time.sleep(0.2)
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if 'ser' in locals(): ser.close()

if __name__ == '__main__':
    ler_serial()
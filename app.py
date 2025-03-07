import time
import psycopg2
import requests
from datetime import datetime

def link():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    dados = response.json()
    return dados

def price(dados):
    valor = float(dados['data']['amount'])  # Convertendo para número
    BTC = dados['data']['base']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return [{'Valor': valor, 'BTC': BTC, 'timestamp': timestamp}]

def inserir_dados(dados_tratados):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Digiteasuasenha',  # Proteja sua senha!
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()

        query = "INSERT INTO bitcoin (valor, moeda, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(query, (
            dados_tratados[0]['Valor'],
            dados_tratados[0]['BTC'],  # 🔹 Força UTF-8
            dados_tratados[0]['timestamp']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Dados inseridos com sucesso!")

    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")

if __name__ == "__main__":
    while True:
        dados = link()
        dados_tratados = price(dados)
        print(dados_tratados)

        inserir_dados(dados_tratados)

        time.sleep(5)  # Pausa de 5 segundos

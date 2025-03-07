# Inserindo dados de uma API em um banco de dados local.
-----------------------------------------------------------------------
## 📋 Descrição

  - Pense no seguinte caso: seu gestor pede para você atualizar algum valor no banco de dados,por exemplo o valor do dolar ou do Bitcon. 
  - Esse processo é manual e esssas moedas podem sofrer flutuações bruncas durante o dia.
  - Nessa caso um saída seria automatizar essa tarefa. Para isso é possível utilizar uma API, para coletar os e utilzar o python para inserir no banco de dados.

  
## 📖 Importante Biblibotecas 

      import time 
      import psycopg2 
      import requests 
      from datetime import datetime

## 📃 Acessando os dados dados da API 

- Foi criada uma função para isso que irá retomar o dados de valor atual do bitcoin 

      def link():
          url = "https://api.coinbase.com/v2/prices/spot"
          response = requests.get(url)
          dados = response.json()
          return dados

- Foi adicionado a coluna de timestamp, utiliando a biblioteca datetim. Já que a API não retornava o hoário.

      def price(dados):
          valor = float(dados['data']['amount'])  # Convertendo para número
          BTC = dados['data']['base']
          timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      
          return [{'Valor': valor, 'BTC': BTC, 'timestamp': timestamp}]

- um Função para inserir os valores coletados na API no Banco de Dados, utilizando a biblioteca psycopg2. Foi inserido os dados em Database local (Postgresql). 

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

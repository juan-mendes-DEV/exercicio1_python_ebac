import csv
import json
import os
import time
from datetime import datetime
from random import uniform
from sys import argv

import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

# URL da API do Banco Central para obter a taxa CDI
BCB_API_URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

def extrair_taxa_cdi():
    """Extrai a taxa CDI da API do Banco Central."""
    try:
        response = requests.get(url=BCB_API_URL)
        response.raise_for_status()
        dados = json.loads(response.text)
        return float(dados[-1]['valor'])  # Retorna o valor mais recente
    except requests.exceptions.RequestException as exc:
        print(f"Erro ao obter dados da API: {exc}")
        return None
    except (KeyError, ValueError) as exc:
        print(f"Erro ao processar os dados da API: {exc}")
        return None

def gerar_csv():
    """Gera e salva um arquivo CSV com os dados da taxa CDI."""
    taxa_cdi = extrair_taxa_cdi()
    if taxa_cdi is None:
        print("Taxa CDI não disponível. Encerrando.")
        return

    arquivo_csv = './taxa-cdi.csv'
    arquivo_existe = os.path.exists(arquivo_csv)

    with open(arquivo_csv, mode='a', encoding='utf-8', newline='') as fp:
        writer = csv.writer(fp)
        if not arquivo_existe:
            # Escreve o cabeçalho se o arquivo não existir
            writer.writerow(['data', 'hora', 'taxa'])

        for _ in range(10):  # Gerar 10 entradas simuladas
            data_hora_atual = datetime.now()
            data = data_hora_atual.strftime('%Y-%m-%d')
            hora = data_hora_atual.strftime('%H:%M:%S')
            taxa_simulada = taxa_cdi + uniform(-0.5, 0.5)  # Adiciona variação aleatória
            writer.writerow([data, hora, round(taxa_simulada, 4)])
            time.sleep(1)  # Espera 1 segundo entre cada entrada

    print(f"Arquivo CSV '{arquivo_csv}' gerado com sucesso.")

def gerar_grafico(nome_grafico):
    """Gera e salva um gráfico com os dados do arquivo CSV."""
    arquivo_csv = './taxa-cdi.csv'

    if not os.path.exists(arquivo_csv):
        print(f"Arquivo '{arquivo_csv}' não encontrado. Por favor, gere o CSV primeiro.")
        return

    df = pd.read_csv(arquivo_csv)
    plt.figure(figsize=(10, 6))
    grafico = sns.lineplot(x='hora', y='taxa', data=df, marker="o")
    grafico.set_title("Taxa CDI ao longo do tempo")
    grafico.set_xlabel("Hora")
    grafico.set_ylabel("Taxa CDI")
    grafico.set_xticklabels(labels=df['hora'], rotation=45)

    arquivo_grafico = f"{nome_grafico}.png"
    plt.tight_layout()
    plt.savefig(arquivo_grafico)
    plt.close()
    print(f"Gráfico salvo como '{arquivo_grafico}'.")

def main():
    if len(argv) < 2:
        print("Uso: python script.py <nome_do_grafico>")
        return

    nome_grafico = argv[1]

    # Gera o arquivo CSV com os dados da taxa CDI
    gerar_csv()

    # Gera o gráfico com o nome fornecido
    gerar_grafico(nome_grafico)

if __name__ == "__main__":
    main()

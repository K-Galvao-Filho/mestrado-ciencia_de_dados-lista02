import pandas as pd
import gzip
import os

def carregar_dados(caminho_arquivo_gz, caminho_saida_csv="email-Eu-core-temporal.csv"):
    """
    Descomprime o arquivo .gz, lê o arquivo de texto e converte para CSV.
    Args:
        caminho_arquivo_gz (str): Caminho para o arquivo .gz.
        caminho_saida_csv (str): Caminho onde o CSV será salvo.
    Returns:
        pd.DataFrame: DataFrame com colunas 'origem', 'destino', 'timestamp'.
    """
    if os.path.exists(caminho_saida_csv):
        print(f"Carregando CSV existente: {caminho_saida_csv}")
        dados = pd.read_csv(caminho_saida_csv)
        return dados
    
    try:
        with gzip.open(caminho_arquivo_gz, 'rt') as arquivo:
            dados = pd.read_csv(arquivo, sep='\s+', names=['origem', 'destino', 'timestamp'], engine='python')
        dados.to_csv(caminho_saida_csv, index=False)
        print(f"Dados convertidos e salvos como: {caminho_saida_csv}")
        print(f"Dataset carregado com {len(dados)} arestas.")
        return dados
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo_gz} não encontrado.")
        raise
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        raise
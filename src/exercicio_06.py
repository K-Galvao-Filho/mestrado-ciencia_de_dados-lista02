import pandas as pd
import matplotlib.pyplot as plt
import os

def exercicio_6(dados, nos_principais):
    """
    Plota o número de arestas de entrada ao longo de 803 dias para os nós principais.
    Args:
        dados (pd.DataFrame): DataFrame com as arestas da rede.
        nos_principais (dict): Nós com maior grau de entrada por comunidade.
    """
    dados['dia'] = dados['timestamp'] // (24 * 3600)
    
    plt.figure(figsize=(12, 6))
    for id_comunidade, no in nos_principais.items():
        arestas_no = dados[dados['destino'] == no]
        contagem_diaria = arestas_no.groupby('dia').size()
        contagem_diaria = contagem_diaria.reindex(range(803), fill_value=0)
        plt.plot(contagem_diaria.index, contagem_diaria.values, label=f"Nó {no} (Comunidade {id_comunidade})")
    
    plt.xlabel("Dia")
    plt.ylabel("Número de E-mails Recebidos")
    plt.title("E-mails Recebidos ao Longo do Tempo")
    plt.legend()
    nome_arquivo = os.path.join("figuras", "exercicio_06_temporal.png")
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Visualização temporal salva como '{nome_arquivo}'.")
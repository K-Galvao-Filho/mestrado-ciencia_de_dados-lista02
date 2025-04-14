import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

def exercicio_2(dados, tipo_layout="spring"):
    """
    Visualiza a rede social direcionada com diferentes layouts.
    Args:
        dados (pd.DataFrame): DataFrame com as arestas da rede.
        tipo_layout (str): Tipo de layout ('spring', 'kamada', 'circular').
    """
    grafo = nx.DiGraph()
    arestas = dados[['origem', 'destino']].values
    grafo.add_edges_from(arestas)
    
    plt.figure(figsize=(10, 10))
    
    if tipo_layout == "spring":
        posicao = nx.spring_layout(grafo, k=0.15, iterations=20)
        nome_arquivo = os.path.join("figuras", "exercicio_02_rede_spring.png")
        titulo = "Rede de E-mails Direcionada (Spring Layout)"
    elif tipo_layout == "kamada":
        posicao = nx.kamada_kawai_layout(grafo)
        nome_arquivo = os.path.join("figuras", "exercicio_02_rede_kamada.png")
        titulo = "Rede de E-mails Direcionada (Kamada-Kawai Layout)"
    elif tipo_layout == "circular":
        posicao = nx.circular_layout(grafo)
        nome_arquivo = os.path.join("figuras", "exercicio_02_rede_circular.png")
        titulo = "Rede de E-mails Direcionada (Circular Layout)"
    else:
        print("Layout inválido. Usando spring como padrão.")
        posicao = nx.spring_layout(grafo, k=0.15, iterations=20)
        nome_arquivo = os.path.join("figuras", "exercicio_02_rede_spring.png")
        titulo = "Rede de E-mails Direcionada (Spring Layout)"
    
    nx.draw(grafo, posicao, node_size=50, arrows=True, with_labels=False)
    plt.title(titulo)
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Visualização da rede salva como '{nome_arquivo}'.")
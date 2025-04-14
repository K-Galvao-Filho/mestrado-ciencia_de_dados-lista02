import pandas as pd
import networkx as nx
from networkx.algorithms.community import louvain_partitions

def exercicio_5(dados):
    """
    Detecta comunidades usando o algoritmo de Louvain do NetworkX e encontra o nó principal por maior grau de entrada.
    Args:
        dados (pd.DataFrame): DataFrame com as arestas da rede.
    Returns:
        dict: Dicionário mapeando ID da comunidade para o nó principal.
    """
    # Cria o grafo direcionado
    grafo = nx.DiGraph()
    arestas = dados[['origem', 'destino']].values
    grafo.add_edges_from(arestas)
    
    # Converte para grafo não direcionado para detecção de comunidades
    grafo_nao_direcionado = grafo.to_undirected()
    
    # Usa louvain_partitions para detectar comunidades
    particoes = louvain_partitions(grafo_nao_direcionado, seed=42)  # seed para reprodutibilidade
    
    # Seleciona a primeira partição (ou a com maior modularidade, se necessário)
    particao = next(particoes)  # Pega a primeira partição
    
    # Organiza nós por comunidade
    comunidades = {}
    for id_comunidade, comunidade in enumerate(particao):
        comunidades[id_comunidade] = list(comunidade)
    
    # Encontra o nó principal por maior grau de entrada em cada comunidade
    nos_principais = {}
    for id_comunidade, nos in comunidades.items():
        graus = grafo.in_degree()
        nome_criterio = "maior grau de entrada"
        graus_comunidade = [(no, graus[no]) for no in nos if no in grafo.nodes()]
        if graus_comunidade:  # Verifica se a comunidade não está vazia
            no_principal = max(graus_comunidade, key=lambda x: x[1])[0]
            nos_principais[id_comunidade] = no_principal
            print(f"Comunidade {id_comunidade}: Nó {no_principal} com {nome_criterio}")
        else:
            print(f"Comunidade {id_comunidade}: Nenhuma aresta de entrada encontrada")
    
    print(f"Nós selecionados por {nome_criterio} são centrais em suas comunidades.")
    return nos_principais
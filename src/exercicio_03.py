import pandas as pd
import networkx as nx

def exercicio_3(dados):
    """
    Calcula a média dos menores caminhos na rede direcionada e analisa conectividade e eficiência.
    Args:
        dados (pd.DataFrame): DataFrame com as arestas da rede.
    Returns:
        float: Média dos menores caminhos (maior componente conexo ou grafo completo).
    """
    # Usa grafo direcionado para refletir a rede de e-mails
    grafo = nx.DiGraph()
    arestas = dados[['origem', 'destino']].values
    grafo.add_edges_from(arestas)
    
    # Verifica se o grafo é fortemente conectado (para DiGraph)
    if nx.is_strongly_connected(grafo):
        media_caminhos = nx.average_shortest_path_length(grafo)
        print(f"Média dos menores caminhos (grafo completo): {media_caminhos:.4f}")
    else:
        # Usa o maior componente fortemente conexo
        maior_componente = max(nx.strongly_connected_components(grafo), key=len)
        grafo_componente = grafo.subgraph(maior_componente).copy()
        media_caminhos = nx.average_shortest_path_length(grafo_componente)
        print(f"Média dos menores caminhos (maior componente fortemente conexo): {media_caminhos:.4f}")
    
    # Interpretação detalhada
    print("\nAnálise da conectividade e eficiência:")
    if media_caminhos < 6:
        print(f"A média de {media_caminhos:.4f} indica alta conectividade (característica de mundo pequeno).")
        print("E-mails tendem a alcançar destinatários com poucos intermediários, sugerindo comunicação eficiente.")
    else:
        print(f"A média de {media_caminhos:.4f} sugere conectividade moderada a baixa.")
        print("A comunicação pode ser menos eficiente, exigindo mais intermediários para e-mails entre nós distantes.")
    print("Em redes sociais, médias abaixo de 6 são comuns, como no conceito de 'seis graus de separação'.")
    
    return media_caminhos
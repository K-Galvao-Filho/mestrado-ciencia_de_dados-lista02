import pandas as pd
import networkx as nx

def exercicio_4(dados):
    """
    Calcula os top 5 nós com base em diferentes métricas de centralidade.
    Args:
        dados (pd.DataFrame): DataFrame com as arestas da rede.
        metrica (str): 'betweenness', 'degree', ou 'closeness'.
    Returns:
        list: Lista de tuplas (nó, valor) para os 5 principais nós.
    """
    grafo = nx.DiGraph()
    arestas = dados[['origem', 'destino']].values
    grafo.add_edges_from(arestas)
     
    centralidade = nx.betweenness_centrality(grafo)
    nome_metrica = "centralidade de intermediação"

    top_5 = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"Top 5 nós por {nome_metrica}:")
    for no, valor in top_5:
        print(f"Nó {no}: {valor:.4f}")
        print("Nós com alta intermediação conectam grupos distintos.")
    
    print("\nInterpretação no contexto da instituição de pesquisa:")
    print("A centralidade de intermediação mede a frequência com que um nó aparece nos menores caminhos entre outros nós na rede de e-mails.")
    print("Nós com alta centralidade são cruciais para o fluxo de informações, funcionando como pontes entre diferentes grupos ou departamentos.")
    print("\nPossíveis papéis desses nós incluem:")
    print("- **Líderes de pesquisa**: Conectam equipes interdisciplinares, promovendo colaboração em projetos acadêmicos.")
    print("- **Administradores**: Coordenam comunicações institucionais, como anúncios ou decisões estratégicas.")
    print("- **Sistemas centrais**: Servidores de e-mail ou newsletters que disseminam informações amplamente.")
    print("\nEstrutura da rede de comunicação:")
    print("A presença de nós com alta centralidade sugere uma rede integrada, onde a colaboração entre departamentos é facilitada.")
    print("No entanto, a rede é centralizada, dependendo de poucos nós críticos. Isso implica:")
    print("- **Eficiência**: Informações fluem rapidamente através desses nós, agilizando a troca de conhecimento.")
    print("- **Vulnerabilidade**: A sobrecarga ou ausência desses nós pode fragmentar a comunicação, isolando grupos e dificultando a colaboração.")
    print("\nImplicações:")
    print("Esses nós são pontos estratégicos para a instituição, mas também pontos de risco. Estratégias como descentralizar comunicações ou criar redundâncias podem mitigar dependências.")
        
    return top_5
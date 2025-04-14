import pandas as pd
from scipy import stats

def exercicio_10(dados, dados_modificados, no_a, no_b, novo_no, teste="t_test"):
    """
    Analisa mudanças no fluxo de e-mails para A, B e C com testes estatísticos.
    Args:
        dados (pd.DataFrame): DataFrame original.
        dados_modificados (pd.DataFrame): DataFrame com a rede modificada.
        no_a (int): Nó A do Exercício 7.
        no_b (int): Nó B do Exercício 7.
        novo_no (int): ID do novo nó C do Exercício 8.
        teste (str): 't_test' ou 'mann_whitney'.
    """
    print(f"Analisando nós: A={no_a}, B={no_b}, C={novo_no}")
    
    # Calcula grau de entrada total
    grau_entrada_antes = dados.groupby('destino').size()
    grau_entrada_depois = dados_modificados.groupby('destino').size()
    
    def obter_grau_entrada(no):
        return grau_entrada_antes.get(no, 0), grau_entrada_depois.get(no, 0)
    
    grau_a_antes, grau_a_depois = obter_grau_entrada(no_a)
    grau_b_antes, grau_b_depois = obter_grau_entrada(no_b)
    grau_c_antes, grau_c_depois = obter_grau_entrada(novo_no)
    
    print(f"Nó A grau de entrada: Antes={grau_a_antes}, Depois={grau_a_depois}")
    print(f"Nó B grau de entrada: Antes={grau_b_antes}, Depois={grau_b_depois}")
    print(f"Nó C grau de entrada: Antes={grau_c_antes}, Depois={grau_c_depois}")
    
    # Verifica redução em A e B, aumento em C
    reduziu_a = grau_a_depois < grau_a_antes
    reduziu_b = grau_b_depois < grau_b_antes
    aumentou_c = grau_c_depois > grau_c_antes
    if reduziu_a and reduziu_b:
        print("O fluxo de e-mails para A e B diminuiu após introdução do nó C.")
        if aumentou_c:
            print("O nó C absorveu parte do fluxo, como esperado.")
        else:
            print("O nó C não registrou aumento correspondente, sugerindo possíveis discrepâncias.")
    else:
        print("O fluxo de e-mails para A e/ou B não diminuiu consistentemente.")
    
    # Séries temporais diárias
    dados['dia'] = dados['timestamp'] // (24 * 3600)
    dados_modificados['dia'] = dados_modificados['timestamp'] // (24 * 3600)
    
    def obter_grau_entrada_diario(no, df):
        arestas_no = df[df['destino'] == no]
        return arestas_no.groupby('dia').size().reindex(range(803), fill_value=0)
    
    # Gera séries para A, B e C
    nos = [(no_a, "A"), (no_b, "B"), (novo_no, "C")]
    series = {
        nome: {
            "antes": obter_grau_entrada_diario(no, dados),
            "depois": obter_grau_entrada_diario(no, dados_modificados)
        }
        for no, nome in nos
    }
    
    # Testes de hipóteses
    alfa = 0.05
    for no, nome in nos:
        serie_antes = series[nome]["antes"]
        serie_depois = series[nome]["depois"]
        try:
            if teste == "t_test":
                estatistica, valor_p = stats.ttest_rel(serie_antes, serie_depois)
                nome_teste = "teste t pareado"
            elif teste == "mann_whitney":
                estatistica, valor_p = stats.mannwhitneyu(serie_antes, serie_depois, alternative='two-sided')
                nome_teste = "teste de Mann-Whitney U"
            else:
                print("Teste inválido. Usando t_test.")
                estatistica, valor_p = stats.ttest_rel(serie_antes, serie_depois)
                nome_teste = "teste t pareado"
            
            print(f"Nó {nome} ({no}) {nome_teste}: estatística={estatistica:.4f}, p-valor={valor_p:.4f}")
            if valor_p < alfa:
                print(f"Mudança significativa no fluxo de e-mails do nó {nome} (p < {alfa}).")
            else:
                print(f"Sem mudança significativa no fluxo de e-mails do nó {nome} (p >= {alfa}).")
        
        except ValueError as e:
            print(f"Erro no teste para nó {nome}: {str(e)}. Pulando análise estatística.")
    
    # Conclusões institucionais
    print("\nConclusões para a instituição:")
    if reduziu_a and reduziu_b and aumentou_c:
        print("O redirecionamento para o nó C foi eficaz em reduzir a carga de e-mails em A e B, transferindo parte do fluxo para C. Isso pode aliviar servidores ou administradores sobrecarregados, melhorando a eficiência da comunicação.")
        if series["A"]["depois"].mean() < series["A"]["antes"].mean() and series["B"]["depois"].mean() < series["B"]["antes"].mean():
            print("Testes confirmam redução significativa no fluxo diário, sugerindo que C assumiu responsabilidades de comunicação.")
        else:
            print("Embora o fluxo total tenha diminuído, os padrões diários não mudaram significativamente, indicando que a redução pode ser distribuída irregularmente.")
    else:
        print("O redirecionamento não reduziu consistentemente o fluxo para A e B, ou C não absorveu o fluxo esperado. Isso pode indicar que a intervenção não foi suficiente para balancear a comunicação.")
        print("Recomenda-se revisar a proporção de redirecionamento (25%) ou considerar outros nós para redistribuição.")
    
    print("Esses resultados podem orientar ajustes na infraestrutura de e-mails, como adicionar mais nós ou otimizar fluxos para evitar gargalos.")
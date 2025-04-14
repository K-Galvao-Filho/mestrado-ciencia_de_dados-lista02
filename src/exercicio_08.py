import pandas as pd
import random

def exercicio_8(dados, no_a, no_b):
    """
    Cria nó C e redireciona aleatoriamente 25% das arestas de A e B para C.
    Args:
        dados (pd.DataFrame): DataFrame com as arestas da rede.
        no_a (int): Nó A selecionado no Exercício 7.
        no_b (int): Nó B selecionado no Exercício 7.
    Returns:
        tuple: DataFrame modificado e ID do novo nó C.
    """
    print(f"Usando nós do Exercício 7: A={no_a}, B={no_b}")
    
    # Cria o novo nó C
    novo_no = max(dados['origem'].max(), dados['destino'].max()) + 1
    print(f"Criando novo nó C: {novo_no}")
    
    # Cria uma cópia do DataFrame para modificações
    dados_modificados = dados.copy()
    
    def redirecionar_arestas(no):
        """Redireciona aleatoriamente 25% das arestas destinadas ao nó para novo_no."""
        arestas_no = dados_modificados[dados_modificados['destino'] == no]
        num_arestas = len(arestas_no)
        num_redirecionar = int(0.25 * num_arestas)
        if num_redirecionar == 0:
            print(f"Nenhuma aresta redirecionada para nó {no} (menos de 4 arestas).")
            return
        
        # Seleciona aleatoriamente 25% das arestas
        indices = arestas_no.sample(n=num_redirecionar, random_state=42).index
        dados_modificados.loc[indices, 'destino'] = novo_no
        print(f"Redirecionadas {num_redirecionar} arestas do nó {no} por amostragem aleatória.")
    
    # Redireciona arestas para A e B
    redirecionar_arestas(no_a)
    redirecionar_arestas(no_b)
    
    return dados_modificados, novo_no
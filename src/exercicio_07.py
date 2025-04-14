import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import os
import random

def exercicio_7(dados, nos_principais):
    """
    Decompõe séries temporais de dois nós escolhidos aleatoriamente, compara tendência e sazonalidade,
    e retorna os nós para uso posterior.
    Args:
        dados (pd.DataFrame): DataFrame com as arestas da rede (origem, destino, timestamp).
        nos_principais (dict): Nós com maior grau de entrada por comunidade.
    Returns:
        tuple: (no_a, no_b), IDs dos nós selecionados.
    """
    # Seleciona dois nós aleatoriamente
    random.seed(42)  # Para reprodutibilidade
    try:
        nos = random.sample(list(nos_principais.values()), k=2)
    except ValueError as e:
        print(f"Erro ao selecionar nós: {str(e)}. Usando nós padrão ou repetidos.")
        nos = list(nos_principais.values())[:2]
        if len(nos) < 2:
            nos = [nos[0], nos[0]] if nos else [0, 0]
    
    no_a, no_b = nos
    print(f"Nós selecionados: A={no_a}, B={no_b}")
    
    # Converte timestamps para dias
    dados['dia'] = dados['timestamp'] // (24 * 3600)
    max_dias = 803  # Período total da rede (fixo para consistência)
    
    def obter_serie_temporal(no):
        """Obtém a série temporal de arestas de entrada para um nó."""
        arestas_no = dados[dados['destino'] == no]
        contagem_diaria = arestas_no.groupby('dia').size()
        return contagem_diaria.reindex(range(max_dias), fill_value=0)
    
    try:
        # Obtém séries temporais
        serie_a = obter_serie_temporal(no_a)
        serie_b = obter_serie_temporal(no_b)
        
        # Decomposição: modelo aditivo, período semanal
        modelo = "additive"
        periodo_sazonal = 7
        decomp_a = seasonal_decompose(serie_a, model=modelo, period=periodo_sazonal, extrapolate_trend='freq')
        decomp_b = seasonal_decompose(serie_b, model=modelo, period=periodo_sazonal, extrapolate_trend='freq')
        
        # Gera visualizações
        for no, decomp in [(no_a, decomp_a), (no_b, decomp_b)]:
            plt.figure(figsize=(12, 8))
            plt.subplot(411)
            plt.plot(decomp.observed, label='Observado')
            plt.legend(loc='best')
            plt.subplot(412)
            plt.plot(decomp.trend, label='Tendência')
            plt.legend(loc='best')
            plt.subplot(413)
            plt.plot(decomp.seasonal, label='Sazonalidade')
            plt.legend(loc='best')
            plt.subplot(414)
            plt.plot(decomp.resid, label='Ruído')
            plt.legend(loc='best')
            nome_arquivo = os.path.join("figuras", f"exercicio_07_no_{no}.png")
            plt.suptitle(f"Decomposição da Série Temporal - Nó {no} (Período Semanal, Modelo Aditivo)")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.savefig(nome_arquivo)
            plt.close()
            print(f"Gráfico salvo como '{nome_arquivo}'.")
        
        # Compara tendências e sazonalidades
        correlacao_tendencia = np.corrcoef(decomp_a.trend, decomp_b.trend)[0, 1]
        correlacao_sazonalidade = np.corrcoef(decomp_a.seasonal, decomp_b.seasonal)[0, 1]
        print(f"\nCorrelação entre nós A={no_a} e B={no_b}:")
        print(f"  Tendência: {correlacao_tendencia:.4f}")
        print(f"  Sazonalidade: {correlacao_sazonalidade:.4f}")
        
        # Conclusões interpretativas
        print("\nInterpretação no contexto da instituição:")
        if abs(correlacao_tendencia) > 0.7:
            print(f"A alta correlação de tendência ({correlacao_tendencia:.4f}) indica que A e B têm padrões de longo prazo semelhantes. Eles podem ser líderes ou departamentos centrais com fluxos de e-mails sincronizados, como grupos de pesquisa colaborativos.")
        else:
            print(f"A baixa correlação de tendência ({correlacao_tendencia:.4f}) sugere que A e B têm dinâmicas distintas. Eles podem representar áreas diferentes, como administração e pesquisa, com demandas de comunicação independentes.")
        
        if abs(correlacao_sazonalidade) > 0.7:
            print(f"A alta correlação de sazonalidade ({correlacao_sazonalidade:.4f}) mostra que A e B seguem ciclos semanais similares, possivelmente devido a rotinas institucionais compartilhadas, como reuniões ou relatórios.")
        else:
            print(f"A baixa correlação de sazonalidade ({correlacao_sazonalidade:.4f}) indica ciclos distintos, talvez com um nó ativo em dias úteis e outro com picos esporádicos, refletindo funções variadas.")
        
        print("Esses padrões sugerem estratégias para otimizar a comunicação, como sincronizar fluxos para nós correlacionados ou diversificar canais para nós independentes.")
    
    except ValueError as e:
        print(f"Erro na análise temporal: {str(e)}. Não foi possível completar a decomposição.")
        return None, None
    
    return no_a, no_b
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import os

def exercicio_9(dados_modificados, no_a, no_b, novo_no):
    """
    Repete a decomposição das séries temporais para os nós A, B e C após modificação, compara tendências e sazonalidades, e tira conclusões.
    Args:
        dados_modificados (pd.DataFrame): DataFrame com a rede modificada.
        no_a (int): Nó A do Exercício 7.
        no_b (int): Nó B do Exercício 7.
        novo_no (int): ID do novo nó C do Exercício 8.
    """
    nos = [no_a, no_b, novo_no]
    print(f"Nós analisados: A={no_a}, B={no_b}, C={novo_no}")
    
    # Converte timestamps para dias
    dados_modificados['dia'] = dados_modificados['timestamp'] // (24 * 3600)
    
    def obter_serie_temporal(no):
        """Obtém a série temporal de arestas de entrada para um nó."""
        arestas_no = dados_modificados[dados_modificados['destino'] == no]
        contagem_diaria = arestas_no.groupby('dia').size()
        return contagem_diaria.reindex(range(803), fill_value=0)
    
    try:
        # Configuração fixa: modelo aditivo, período 7 dias
        modelo = "additive"
        periodo = 7
        
        # Decompõe as séries temporais para A, B e C
        series = {no: obter_serie_temporal(no) for no in nos}
        decomps = {
            no: seasonal_decompose(serie, model=modelo, period=periodo, extrapolate_trend='freq')
            for no, serie in series.items()
        }
        
        # Gera visualizações para cada nó
        for no in nos:
            decomp = decomps[no]
            plt.figure(figsize=(12, 8))
            plt.subplot(411)
            plt.plot(decomp.observed, label='Observado')
            plt.legend()
            plt.subplot(412)
            plt.plot(decomp.trend, label='Tendência')
            plt.legend()
            plt.subplot(413)
            plt.plot(decomp.seasonal, label='Sazonalidade')
            plt.legend()
            plt.subplot(414)
            plt.plot(decomp.resid, label='Ruído')
            plt.legend()
            nome_arquivo = os.path.join("figuras", f"exercicio_09_no_{no}_modificado.png")
            plt.suptitle(f"Decomposição da Série Temporal para Nó {no} (Modificado, Período=7, Modelo=aditivo)")
            plt.savefig(nome_arquivo)
            plt.close()
            print(f"Decomposição salva como '{nome_arquivo}'.")
        
        # Compara tendências e sazonalidades (A vs. B, A vs. C, B vs. C)
        pares = [("A vs. B", no_a, no_b), ("A vs. C", no_a, novo_no), ("B vs. C", no_b, novo_no)]
        for nome_par, n1, n2 in pares:
            correlacao_tendencia = np.corrcoef(decomps[n1].trend, decomps[n2].trend)[0, 1]
            correlacao_sazonalidade = np.corrcoef(decomps[n1].seasonal, decomps[n2].seasonal)[0, 1]
            print(f"\nCorrelações para {nome_par}:")
            print(f"  Tendência: {correlacao_tendencia:.4f}")
            print(f"  Sazonalidade: {correlacao_sazonalidade:.4f}")
        
        # Conclusões interpretativas
        print("\nInterpretação dos resultados após redirecionamento:")
        # A vs. B
        correlacao_tendencia_ab = np.corrcoef(decomps[no_a].trend, decomps[no_b].trend)[0, 1]
        correlacao_sazonalidade_ab = np.corrcoef(decomps[no_a].seasonal, decomps[no_b].seasonal)[0, 1]
        if abs(correlacao_tendencia_ab) > 0.7:
            print(f"A alta correlação da tendência entre A e B ({correlacao_tendencia_ab:.4f}) sugere que o redirecionamento para C não alterou significativamente seus padrões de longo prazo. Eles continuam desempenhando papéis complementares.")
        else:
            print(f"A baixa correlação da tendência entre A e B ({correlacao_tendencia_ab:.4f}) indica que o redirecionamento pode ter diferenciado ainda mais suas dinâmicas de longo prazo, talvez reduzindo interdependências.")
        
        if abs(correlacao_sazonalidade_ab) > 0.7:
            print(f"A alta correlação da sazonalidade entre A e B ({correlacao_sazonalidade_ab:.4f}) implica que os ciclos semanais permanecem sincronizados, apesar do redirecionamento para C.")
        else:
            print(f"A baixa correlação da sazonalidade entre A e B ({correlacao_sazonalidade_ab:.4f}) sugere que o redirecionamento alterou os ciclos temporais, possivelmente redistribuindo picos de e-mails.")
        
        # Impacto em C
        correlacao_tendencia_ac = np.corrcoef(decomps[no_a].trend, decomps[novo_no].trend)[0, 1]
        correlacao_tendencia_bc = np.corrcoef(decomps[no_b].trend, decomps[novo_no].trend)[0, 1]
        correlacao_sazonalidade_ac = np.corrcoef(decomps[no_a].seasonal, decomps[novo_no].seasonal)[0, 1]
        correlacao_sazonalidade_bc = np.corrcoef(decomps[no_b].seasonal, decomps[novo_no].seasonal)[0, 1]
        
        if abs(correlacao_tendencia_ac) > 0.7 or abs(correlacao_tendencia_bc) > 0.7:
            print(f"A tendência de C é semelhante à de A ({correlacao_tendencia_ac:.4f}) ou B ({correlacao_tendencia_bc:.4f}), indicando que C assumiu parte do papel de longo prazo de um dos nós originais.")
        else:
            print(f"A tendência de C é distinta de A ({correlacao_tendencia_ac:.4f}) e B ({correlacao_tendencia_bc:.4f}), sugerindo que C opera de forma independente em longo prazo.")
        
        if abs(correlacao_sazonalidade_ac) > 0.7 or abs(correlacao_sazonalidade_bc) > 0.7:
            print(f"A sazonalidade de C é semelhante à de A ({correlacao_sazonalidade_ac:.4f}) ou B ({correlacao_sazonalidade_bc:.4f}), mostrando que C herdou ciclos semanais de pelo menos um dos nós.")
        else:
            print(f"A sazonalidade de C é distinta de A ({correlacao_sazonalidade_ac:.4f}) e B ({correlacao_sazonalidade_bc:.4f}), indicando que C tem padrões cíclicos próprios.")
        
        print("O redirecionamento para C pode ter redistribuído a carga de comunicação, afetando estratégias institucionais, como balanceamento de servidores ou fluxos de e-mails.")
    
    except ValueError as e:
        print(f"Erro na decomposição: {str(e)}. Não foi possível completar a análise.")
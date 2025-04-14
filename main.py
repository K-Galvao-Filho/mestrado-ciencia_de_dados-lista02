import os
from src.carregar_dados import carregar_dados
from src.exercicio_02 import exercicio_2
from src.exercicio_03 import exercicio_3
from src.exercicio_04 import exercicio_4
from src.exercicio_05 import exercicio_5
from src.exercicio_06 import exercicio_6
from src.exercicio_07 import exercicio_7
from src.exercicio_08 import exercicio_8
from src.exercicio_09 import exercicio_9
from src.exercicio_10 import exercicio_10

def main():
    """
    Função principal que executa todos os exercícios, criando a pasta 'figuras' e coordenando a execução.
    """
    # Cria a pasta 'figuras' se não existir
    pasta_figuras = "figuras"
    os.makedirs(pasta_figuras, exist_ok=True)
    
    # Caminhos dos arquivos
    caminho_arquivo_gz = "dados/email-Eu-core-temporal.txt.gz"
    caminho_saida_csv = "dados/email-Eu-core-temporal.csv"
    
    print("Exercício 1: Carregando e convertendo dados")
    dados = carregar_dados(caminho_arquivo_gz, caminho_saida_csv)
    
    print("\nExercício 2: Visualizando a rede")
    exercicio_2(dados)
    
    print("\nExercício 3: Analisando métricas globais")
    exercicio_3(dados)

    print("\nExercício 4: Analisando métricas estruturais")
    exercicio_4(dados)
    
    print("\nExercício 5: Detectando comunidades")
    nos_principais = exercicio_5(dados)
    
    print("\nExercício 6: Visualização temporal")
    exercicio_6(dados, nos_principais)
    
    print("\nExercício 7: Análise de séries temporais")
    no_a, no_b = exercicio_7(dados, nos_principais)

    print("\nExercício 8: Modificando a rede")
    if no_a is not None and no_b is not None:
        dados_modificados, novo_no = exercicio_8(dados, no_a, no_b)
        print("\nExercício 9: Analisando a rede modificada")
        exercicio_9(dados_modificados, no_a, no_b, novo_no)
        print("\nExercício 10: Tomada de decisão")
        exercicio_10(dados, dados_modificados, no_a, no_b, novo_no, teste="t_test")
    else:
        print("Exercícios 8, 9 e 10 não executados devido a erro no Exercício 7.")

if __name__ == "__main__":
    main()
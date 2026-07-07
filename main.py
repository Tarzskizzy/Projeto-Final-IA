from experimentos import executar_experimento
from gerador import gerar_lista_pacientes
from inferencia import avaliar_lista_pacientes
from astar import a_star_triagem
import warnings

# Esconde os avisos vermelhos de depreciação do pgmpy
warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    print("="*60)
    print("SISTEMA INTELIGENTE DE TRIAGEM HOSPITALAR")
    print("="*60)

    # 1. EXECUTAR EXPERIMENTOS (Imprime a comparação de custos na tela)
    executar_experimento(6, "CENÁRIO PEQUENO")
    executar_experimento(20, "CENÁRIO MÉDIO")

    # 2. EXIBIR A FILA ÓTIMA DO A* - CENÁRIO PEQUENO
    print("\n" + "="*60)
    print("ORDEM ÓTIMA DE ATENDIMENTO (A*) - CENÁRIO PEQUENO")
    print("="*60)
    
    pacientes_p = gerar_lista_pacientes(6, seed=42)
    avaliar_lista_pacientes(pacientes_p)
    fila_otima_p, _ = a_star_triagem(pacientes_p)
    
    for i, p in enumerate(fila_otima_p, 1):
        print(f"{i}º: {p}")

    # 3. EXIBIR A FILA ÓTIMA DO A* - CENÁRIO MÉDIO
    print("\n" + "="*60)
    print("ORDEM ÓTIMA DE ATENDIMENTO (A*) - CENÁRIO MÉDIO")
    print("="*60)
    
    pacientes_m = gerar_lista_pacientes(20, seed=42)
    avaliar_lista_pacientes(pacientes_m)
    fila_otima_m, _ = a_star_triagem(pacientes_m)
    
    for i, p in enumerate(fila_otima_m, 1):
        print(f"{i}º: {p}")

if __name__ == "__main__":
    main()

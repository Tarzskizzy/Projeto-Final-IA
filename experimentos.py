from gerador import gerar_lista_pacientes
from inferencia import avaliar_lista_pacientes
from astar import a_star_triagem

def estrategia_fifo(pacientes_lista):
    # Atende na ordem de chegada (maior tempo de espera acumulado)
    return sorted(pacientes_lista, key=lambda x: x.tempo_espera, reverse=True)

def estrategia_gulosa(pacientes_lista):
    # Atende sempre o de maior P(gravidade alta), ignora tempo
    return sorted(pacientes_lista, key=lambda x: x.prob_alta, reverse=True)

def calcular_custo_simulacao(ordem_pacientes, dict_referencia):
    # Calcula o custo da mesma forma que o A* para manter a comparação justa
    custo_total, passos = 0, 0
    restantes = set([p.id for p in ordem_pacientes])
    for p in ordem_pacientes:
        restantes.remove(p.id)
        passos += 1
        custo_passo = sum(dict_referencia[pid].risco * (dict_referencia[pid].tempo_espera + passos) for pid in restantes)
        custo_total += custo_passo
    return custo_total

def executar_experimento(quantidade_pacientes, nome_cenario):
    print(f"\n{'='*60}\n{nome_cenario} ({quantidade_pacientes} PACIENTES)\n{'='*60}")

    lista = gerar_lista_pacientes(quantidade_pacientes, seed=42)
    avaliar_lista_pacientes(lista)

    dict_suporte = {p.id: p for p in lista}

    # FIFO
    fila_fifo = estrategia_fifo(lista)
    custo_fifo = calcular_custo_simulacao(fila_fifo, dict_suporte)
    print(f"-> [FIFO]   Custo Acumulado: {custo_fifo:.2f}")

    # GULOSA
    fila_gulosa = estrategia_gulosa(lista)
    custo_gulosa = calcular_custo_simulacao(fila_gulosa, dict_suporte)
    print(f"-> [GULOSA] Custo Acumulado: {custo_gulosa:.2f}")

    # A* (Mantendo a construção da tupla original)
    fila_otimizada, custo_astar = a_star_triagem(lista)

    if fila_otimizada:
        print(f"-> [A*]     Custo Acumulado: {custo_astar:.2f}")
    else:
        print("-> [A*]     Erro: Não foi possível calcular a fila.")


if __name__ == "__main__":
    # Executa os dois cenários
    executar_experimento(6, "CENÁRIO PEQUENO")
    executar_experimento(20, "CENÁRIO MÉDIO")


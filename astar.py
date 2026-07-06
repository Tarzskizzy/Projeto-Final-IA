import heapq

# Estrutura interna para os nós do A*
class NoAStar:
    def __init__(self, pacientes_restantes, caminho, g, h):
        self.pacientes_restantes = pacientes_restantes  # frozenset de índices (IDs)
        self.caminho = caminho                          # Lista com a ordem dos IDs atendidos
        self.g = g                                      # Custo real acumulado (risco)
        self.h = h                                      # Estimativa heurística restante
        self.f = g + h                                  # Custo total estimado

    def __lt__(self, outro):
        return self.f < outro.f

# Cálculo da Heurística
def calcular_heuristica(ids_restantes, passos_atuais,pacientes_dict):
    """
    Heurística Admissível: Ordena os pacientes restantes pelo maior risco.
    Simula o cenário ideal para estimar o custo mínimo restante de forma otimista.
    """
    if not ids_restantes:
        return 0
    
    # Ordena os restantes pelo maior risco (estratégia gulosa ideal)
    ordenados = sorted(
        [pacientes_dict[pid] for pid in ids_restantes],
        key=lambda x:x.risco,
        reverse=True
    )
    
    custo_h = 0
    passos_simulados = passos_atuais
    restantes_simulados = list(ordenados)
    
    # Simula o esvaziamento da fila no melhor cenário possível
    while len(restantes_simulados) > 1:
        passos_simulados += 1
        restantes_simulados.pop(0) # Atende o de maior risco imediatamente
        
        # Os que continuam esperando acumulam risco baseado no tempo atualizado
        for p in restantes_simulados:
            tempo_atualizado = p.tempo_espera + passos_simulados
            custo_h += p.risco * tempo_atualizado
            
    return custo_h

# Implementação do Algoritmo
def a_star_triagem(lista_pacientes):
    """
    Executa o algoritmo A* para encontrar a ordem ótima de atendimento.
    lista_pacientes: Lista de vetores/tuplas no formato (nivel_de_risco, tempo_de_espera)
    """
    # Mapeia a lista para um dicionário indexado para identificar cada paciente unicamente
    pacientes_dict = {
        paciente.id: paciente
        for paciente in lista_pacientes
    }
    
    total_pacientes = len(lista_pacientes)
    

    # ==========================================
    # Inicialização do A*
    # ==========================================
    ids_iniciais = frozenset(pacientes_dict.keys())
    h_inicial = calcular_heuristica(ids_iniciais, passos_atuais=0,pacientes_dict=pacientes_dict)
    
    no_inicial = NoAStar(pacientes_restantes=ids_iniciais, caminho=[], g=0, h=h_inicial)
    
    open_list = []
    heapq.heappush(open_list, no_inicial)
    closed_set = set()
    
    # Loop de busca do A*
    while open_list:
        no_atual = heapq.heappop(open_list)
        
        # OBJETIVO: Fila vazia (todos atendidos)
        if not no_atual.pacientes_restantes:
            # Retorna a sequência de vetores original ordenada e o custo final
            ordem_final = [pacientes_dict[pid] for pid in no_atual.caminho]
            return ordem_final, no_atual.g
            
        if no_atual.pacientes_restantes in closed_set:
            continue
            
        closed_set.add(no_atual.pacientes_restantes)
        
        # Mede quantos pacientes já foram atendidos até este nó
        passos_atuais = total_pacientes - len(no_atual.pacientes_restantes)
        
        # AÇÃO: Escolher o próximo paciente a ser retirado da fila
        for id_escolhido in no_atual.pacientes_restantes:
            proximos_restantes = no_atual.pacientes_restantes - frozenset([id_escolhido])
            
            # Avança 1 unidade de tempo para o atendimento atual
            proximo_passo = passos_atuais + 1
            
            # CUSTO DA AÇÃO: Risco acumulado de quem CONTINUA esperando
            # Risco do passo = Soma de (Risco * Tempo Atualizado de Espera) para os restantes
            custo_passo = sum(
                pacientes_dict[pid].risco * (pacientes_dict[pid].tempo_espera + proximo_passo)
                for pid in proximos_restantes
            )
            
            proximo_g = no_atual.g + custo_passo
            proximo_h = calcular_heuristica(proximos_restantes, passos_atuais=proximo_passo,pacientes_dict=pacientes_dict)
            proximo_caminho = no_atual.caminho + [id_escolhido]
            
            novo_no = NoAStar(proximos_restantes, proximo_caminho, proximo_g, proximo_h)
            heapq.heappush(open_list, novo_no)
            
    return None, 0


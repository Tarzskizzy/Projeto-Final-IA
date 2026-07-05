import heapq

class Paciente:
    def __init__(self, id_paciente, gravidade, tempo_atendimento, tempo_espera_atual=0):
        self.id = id_paciente
        self.gravidade = gravidade
        self.tempo_atendimento = tempo_atendimento
        self.tempo_espera_atual = tempo_espera_atual # Tempo que já esperou antes da triagem começar

    def __repr__(self):
        return f"Paciente({self.id}, Grav={self.gravidade}, Tempo={self.tempo_atendimento})"


class NoAStar:
    def __init__(self, pacientes_restantes, caminho, g, h):
        self.pacientes_restantes = pacientes_restantes # frozenset com IDs
        self.caminho = caminho # Lista com a ordem dos IDs já atendidos
        self.g = g # Custo acumulado (risco)
        self.h = h # Custo heurístico estimado
        self.f = g + h # Custo total

    # Necessário para o heapq ordenar a fila de prioridades
    def __lt__(self, outro):
        return self.f < outro.f


def calcular_heuristica(ids_restantes, dict_pacientes):
    """
    Heurística admissível: Simula o cenário ideal organizando os pacientes restantes
    pela maior taxa de 'Gravidade por minuto de atendimento'.
    """
    if not ids_restantes:
        return 0
        
    # Filtra os pacientes que ainda estão na fila
    pacientes = [dict_pacientes[pid] for pid in ids_restantes]
    
    # Ordena do maior risco/tempo para o menor (cenário ideal guloso)
    pacientes.sort(key=lambda p: p.gravidade / p.tempo_atendimento, reverse=True)
    
    custo_h = 0
    tempo_acumulado = 0
    
    for p in pacientes:
        # Cada paciente vai esperar o tempo acumulado dos pacientes ideais antes dele
        custo_h += p.gravidade * tempo_acumulado
        tempo_acumulado += p.tempo_atendimento
        
    return custo_h


def a_star_triagem(lista_pacientes):
    # Dicionário de acesso rápido
    dict_pacientes = {p.id: p for p in lista_pacientes}
    
    # Estado inicial
    ids_iniciais = frozenset(dict_pacientes.keys())
    h_inicial = calcular_heuristica(ids_iniciais, dict_pacientes)
    
    # Nó inicial: todos na fila, caminho vazio, g=0
    no_inicial = NoAStar(pacientes_restantes=ids_iniciais, caminho=[], g=0, h=h_inicial)
    
    # Fila de prioridade (Open List)
    open_list = []
    heapq.heappush(open_list, no_inicial)
    
    # Conjunto de estados já avaliados (Closed Set)
    closed_set = set()
    
    while open_list:
        no_atual = heapq.heappop(open_list)
        
        # OBJETIVO: Fila vazia
        if not no_atual.pacientes_restantes:
            return no_atual # Retorna o nó final contendo o caminho ótimo e o custo total
            
        # Se já visitamos essa exata combinação de pacientes restantes, ignoramos
        if no_atual.pacientes_restantes in closed_set:
            continue
            
        closed_set.add(no_atual.pacientes_restantes)
        
        # AÇÃO: Gerar os próximos estados escolhendo cada paciente possível
        for id_escolhido in no_atual.pacientes_restantes:
            paciente_escolhido = dict_pacientes[id_escolhido]
            
            # Remove o paciente escolhido da fila de espera
            proximos_restantes = no_atual.pacientes_restantes - frozenset([id_escolhido])
            
            # CUSTO DA AÇÃO: Risco acumulado dos pacientes que continuam na fila
            # Risco = Soma(Gravidade do paciente i * Tempo de atendimento do escolhido)
            custo_passo = sum(dict_pacientes[pid].gravidade * paciente_escolhido.tempo_atendimento 
                              for pid in proximos_restantes)
            
            proximo_g = no_atual.g + custo_passo
            proximo_h = calcular_heuristica(proximos_restantes, dict_pacientes)
            proximo_caminho = no_atual.caminho + [id_escolhido]
            
            # Cria o novo nó e coloca na fila de prioridades
            novo_no = NoAStar(proximos_restantes, proximo_caminho, proximo_g, proximo_h)
            heapq.heappush(open_list, novo_no)
            
    return None

# ==========================================
# Exemplo de Uso
# ==========================================
if __name__ == "__main__":
    # Criando pacientes fictícios
    # (ID, Gravidade (1 a 10), Tempo de atendimento estimado em minutos, Tempo já esperado)
    fila_de_espera = [
        Paciente("João (Leve)", gravidade=2, tempo_atendimento=10, tempo_espera_atual=30),
        Paciente("Maria (Grave)", gravidade=9, tempo_atendimento=20, tempo_espera_atual=10),
        Paciente("Carlos (Moderado)", gravidade=5, tempo_atendimento=15, tempo_espera_atual=45),
        Paciente("Ana (Crítico)", gravidade=10, tempo_atendimento=5, tempo_espera_atual=5)
    ]

    print("Calculando a melhor fila de triagem com A*...\n")
    resultado = a_star_triagem(fila_de_espera)

    if resultado:
        print("=== ORDEM DE ATENDIMENTO OTIMIZADA ===")
        for i, id_pac in enumerate(resultado.caminho, 1):
            print(f"{i}º a ser atendido: {id_pac}")
        print(f"\nCusto total minimizado (Risco Agregado): {resultado.g}")
    else:
        print("Não foi possível encontrar uma solução.")
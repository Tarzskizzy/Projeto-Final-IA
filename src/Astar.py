# Funcionamento do Algoritmo A* para o trabalho final de IA

# Definição Formal no trabalho
# 1. Estado: Lista de pacientes ainda aguardando, cada um com o vetor gravidade e tempo de espera
# 2. Estado inicial: Todos os pacientes na fila, nenhum atendido ainda
# 3. Ação: escolher o próximo paciente a ser atendido (Remove ele da fila)
# 4. Custo de uma ação: o risco acumulado de todos os pacientes que continuam esperando
# 5. Objetivo: fila vazia - todos os pacientes atendidos
# 6. Heurística h(n): estimativa do custo mínimo restante, a partir do estado atual (ver abaixo)
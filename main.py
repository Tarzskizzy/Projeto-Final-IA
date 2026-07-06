from gerador import gerar_lista_pacientes
from inferencia import avaliar_lista_pacientes
from astar import a_star_triagem

pacientes = gerar_lista_pacientes(30, seed=42)

avaliar_lista_pacientes(pacientes)

fila_otima, custo = a_star_triagem(pacientes)

print("Melhor ordem de atendimento:\n")

for p in fila_otima:
    print(p)
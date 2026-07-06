from pgmpy.inference import VariableElimination
from rede_bayesiana import modelo

inferencia = VariableElimination(modelo)

def avaliar_paciente(paciente):

    resultado = inferencia.query(
        variables=["Gravidade"],
        evidence={
            "Febre": paciente.febre,
            "SaturacaoO2": paciente.saturacao,
            "PressaoArterial": paciente.pressao,
            "IdadeDoenca": paciente.idade_doenca,
            "FreqCardiaca": paciente.freq_cardiaca,
            "NivelDor": paciente.nivel_dor
        }
    )

    paciente.prob_baixa = resultado.values[0]
    paciente.prob_media = resultado.values[1]
    paciente.prob_alta = resultado.values[2]
    paciente.risco = paciente.prob_alta * paciente.tempo_espera
    paciente.risco = paciente.risco

    return paciente

# Função para avaliar as probabilidades de gravidades de todos os pacientes
def avaliar_lista_pacientes(lista):

    for paciente in lista:
        avaliar_paciente(paciente)

    return lista
import numpy as np

# Classe objeto para os pacientes
class Paciente:
    def __init__(self, id, febre, saturacao, pressao,
                 idade_doenca, freq_cardiaca, nivel_dor,
                 tempo_espera, risco):

        self.id = id

        # Sintomas
        self.febre = febre
        self.saturacao = saturacao
        self.pressao = pressao
        self.idade_doenca = idade_doenca
        self.freq_cardiaca = freq_cardiaca
        self.nivel_dor = nivel_dor
        self.risco = 0

        # Tempo de espera (minutos)
        self.tempo_espera = tempo_espera

        # Resultados da Rede Bayesiana
        self.prob_baixa = None
        self.prob_media = None
        self.prob_alta = None

    def mostrar_probabilidades(self):
        return (
            f"Paciente {self.id} | "
            f"Baixa={self.prob_baixa:.2f}, "
            f"Média={self.prob_media:.2f}, "
            f"Alta={self.prob_alta:.2f}"
        )

    def __repr__(self):
        return (
            f"Paciente {self.id} | "
            f"Febre={self.febre}, "
            f"Sat={self.saturacao}, "
            f"Pres. Arterial={self.pressao}, "
            f"Idade={self.idade_doenca}, "
            f"Freq. Cardíaca={self.freq_cardiaca}, "
            f"Dor={self.nivel_dor}, "
            f"Espera={self.tempo_espera} min, "
            f"Risco={self.risco:.2f}"
        )

# Função para gerar um paciente (probabilidades iguais aos dos CPDs)
def gerar_paciente(id):

    febre = np.random.choice(
        [0, 1],
        p=[0.6, 0.4]
    )
    saturacao = np.random.choice(
        [0, 1, 2],
        p=[0.6, 0.3, 0.1]
    )

    pressao = np.random.choice(
        [0, 1],
        p=[0.7, 0.3]
    )

    idade_doenca = np.random.choice(
        [0, 1],
        p=[0.6, 0.4]
    )

    freq_cardiaca = np.random.choice(
        [0, 1],
        p=[0.7, 0.3]
    )

    nivel_dor = np.random.choice(
        [0, 1, 2],
        p=[0.5, 0.3, 0.2]
    )

    risco = None 
    # Tempo de espera entre 5 e 60 minutos
    tempo_espera = np.random.randint(5, 61)

    return Paciente(
        id,
        febre,
        saturacao,
        pressao,
        idade_doenca,
        freq_cardiaca,
        nivel_dor,
        tempo_espera,
        risco
    )

# Função para gerar um número n de pacientes
def gerar_lista_pacientes(n, seed=None):

    if seed is not None:
        np.random.seed(seed)

    pacientes = []

    for i in range(1, n + 1):
        pacientes.append(gerar_paciente(i))

    return pacientes

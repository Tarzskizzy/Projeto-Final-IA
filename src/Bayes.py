import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import itertools

# Conexões de causa e efeito.
# Os sinais vitais apontam para a 'Gravidade'.
modelo = DiscreteBayesianNetwork([
    ('Febre', 'Gravidade'),
    ('SaturacaoO2', 'Gravidade'),
    ('PressaoArterial', 'Gravidade'),
    ('IdadeDoenca', 'Gravidade'),
    ('FreqCardiaca', 'Gravidade'),
    ('NivelDor', 'Gravidade')
])

# probabilidade de um paciente chegar com esse sintoma.
# variable_card indica a quantidade de estados possíveis (ex: 2 = Não/Sim).

cpd_febre = TabularCPD(variable='Febre', variable_card=2, values=[[0.6], [0.4]])
cpd_pressao = TabularCPD(variable='PressaoArterial', variable_card=2, values=[[0.7], [0.3]])
cpd_idade = TabularCPD(variable='IdadeDoenca', variable_card=2, values=[[0.6], [0.4]])
cpd_freq = TabularCPD(variable='FreqCardiaca', variable_card=2, values=[[0.7], [0.3]])
cpd_sat = TabularCPD(variable='SaturacaoO2', variable_card=3, values=[[0.6], [0.3], [0.1]])
cpd_dor = TabularCPD(variable='NivelDor', variable_card=3, values=[[0.5], [0.3], [0.2]])

# Pesos heurísticos inspirados na importância clínica dos sinais vitais
# descrita em protocolos como NEWS e Manchester.

pesos = {
    'Febre': [0, 0.5],
    'SaturacaoO2': [0, 2.0, 4.0],
    'PressaoArterial': [0, 2.0],
    'IdadeDoenca': [0, 1.5],
    'FreqCardiaca': [0, 1.0],
    'NivelDor': [0, 1.0, 2.0]
}

combinacoes = list(itertools.product([0,1], [0,1,2], [0,1], [0,1], [0,1], [0,1,2]))
prob_baixa, prob_media, prob_alta = [], [], []

escore_maximo = (
    max(pesos['Febre']) +
    max(pesos['SaturacaoO2']) +
    max(pesos['PressaoArterial']) +
    max(pesos['IdadeDoenca']) +
    max(pesos['FreqCardiaca']) +
    max(pesos['NivelDor'])
)

for combo in combinacoes:
    # Calcula o escore total do paciente
    escore = (pesos['Febre'][combo[0]] + pesos['SaturacaoO2'][combo[1]] +
             pesos['PressaoArterial'][combo[2]] + pesos['IdadeDoenca'][combo[3]] +
             pesos['FreqCardiaca'][combo[4]] + pesos['NivelDor'][combo[5]])

    # Probabilidade Alta usando função Sigmoide (transição suave)
    # Subtraímos 5 para centralizar a curva sigmoide no escore médio
    centro = escore_maximo / 2

    p_a = 1/(1+np.exp(-(escore-centro)))

    # Probabilidade Baixa decai linearmente conforme o escore sobe
    x = escore / escore_maximo
    p_b = 0.85 * (1 - x) + 0.01

    # Garantir limites lógicos
    p_a = min(max(p_a, 0.02), 0.95)
    p_b = min(max(p_b, 0.01), 0.90)

    # Probabilidade Média fica com o restante
    p_m = max(0.0, 1.0 - p_a - p_b)

    # Normalização final para garantir que a soma da coluna seja exatamente 1.0
    soma = p_a + p_m + p_b
    prob_alta.append(p_a / soma)
    prob_media.append(p_m / soma)
    prob_baixa.append(p_b / soma)

# Montagem da CPT final
cpd_gravidade = TabularCPD(
    variable='Gravidade', variable_card=3,
    evidence=['Febre', 'SaturacaoO2', 'PressaoArterial', 'IdadeDoenca', 'FreqCardiaca', 'NivelDor'],
    evidence_card=[2, 3, 2, 2, 2, 3],
    values=[prob_baixa, prob_media, prob_alta]
)

modelo.add_cpds(cpd_febre, cpd_sat, cpd_pressao, cpd_idade, cpd_freq, cpd_dor, cpd_gravidade)
modelo.check_model()

# Análise e realização da Inferência
inferencia = VariableElimination(modelo)

# Teste para verificar a suavidade da curva:
res_leve = inferencia.query(variables=['Gravidade'], evidence={'Febre':0, 'SaturacaoO2':0, 'PressaoArterial':0, 'IdadeDoenca':0, 'FreqCardiaca':0, 'NivelDor':0})
res_med = inferencia.query(variables=['Gravidade'], evidence={'Febre':0, 'SaturacaoO2':1, 'PressaoArterial':0, 'IdadeDoenca':1, 'FreqCardiaca':0, 'NivelDor':0})
res_grave = inferencia.query(variables=['Gravidade'], evidence={'Febre':0, 'SaturacaoO2':2, 'PressaoArterial':1, 'IdadeDoenca':1, 'FreqCardiaca':1, 'NivelDor':1})

print("Paciente Saudável (Escore 0):\n", res_leve)
print("\nPaciente Intermediário (Escore 3.5):\n", res_med)
print("\nPaciente Grave (Escore 9.5):\n", res_grave)
# Projeto-Final-IA
Projeto final da Disciplina de IA do curso de Ciências de Dados na UFC

# Sistema Inteligente de Triagem Hospitalar

O objetivo é utilizar uma Rede Bayesiana para estimar a gravidade de pacientes e, em seguida, aplicar o algoritmo A* para encontrar a ordem ótima de atendimento, minimizando o risco de deterioração dos pacientes durante a espera.

## Descrição dos módulos

### `main.py`

Arquivo principal do projeto.

É responsável por orquestrar o fluxo completo da aplicação, executando:

Os experimentos comparativos de custo acumulado (FIFO vs. Gulosa vs. A*) para os cenários pequeno (6 pacientes) e médio (20 pacientes), acionando o módulo experimentos.py.

A geração e exibição detalhada da fila com a ordem ótima de atendimento calculada pelo algoritmo A* para ambos os cenários simulados.

---

### `rede_bayesiana.py`

Implementa a Rede Bayesiana do sistema.

Neste módulo são definidos:

- a estrutura da rede;
- os CPDs das variáveis clínicas;
- a CPT da variável Gravidade;
- o modelo probabilístico utilizado durante a inferência.

---

### `inferencia.py`

Responsável pela inferência probabilística utilizando o algoritmo Variable Elimination da biblioteca pgmpy.

Também calcula, para cada paciente:

- Probabilidade de gravidade baixa;
- Probabilidade de gravidade média;
- Probabilidade de gravidade alta;
- Risco de deterioração utilizado pelo algoritmo de busca.

---

### `gerador.py`

Responsável pela criação dos pacientes utilizados nas simulações.

Contém:

- classe `Paciente`;
- geração aleatória dos sinais vitais;
- geração do tempo de espera;
- geração de listas de pacientes.

---

### `astar.py`

Implementa o algoritmo A* responsável por determinar a ordem ótima de atendimento.

Contém:

- estrutura dos nós do algoritmo;
- função heurística;
- função de busca A*.

---

### `experimentos.py`

Implementa os experimentos utilizados para avaliar o desempenho do sistema.

Também contém as estratégias de comparação:

- FIFO;
- Gulosa;
- A*.

Além disso, calcula o custo acumulado de cada estratégia para permitir a comparação dos resultados.

# Algoritmo ACO para o Problema do Caixeiro Viajante (TSP)

Este projeto implementa o algoritmo de Otimização por Colônia de Formigas (ACO - Ant Colony Optimization) para resolver o Problema do Caixeiro Viajante (TSP - Traveling Salesman Problem) com 4 cidades.

## Descrição do Problema

O problema consiste em encontrar o menor caminho possível que passa por todas as 4 cidades (A, B, C e D) exatamente uma vez e retorna à cidade de origem. As distâncias entre as cidades são conhecidas e representadas em um grafo não direcionado.

### Distâncias entre as cidades:
- A → B: 10 unidades
- A → C: 15 unidades
- A → D: 20 unidades
- B → C: 35 unidades
- B → D: 25 unidades
- C → D: 30 unidades

## Algoritmo de Otimização por Colônia de Formigas (ACO)

### Conceito Básico
O ACO é um algoritmo meta-heurístico inspirado no comportamento de formigas reais na busca por alimentos. As formigas depositam feromônios no caminho que percorrem, criando trilhas que podem ser seguidas por outras formigas. Caminhos mais curtos tendem a acumular mais feromônios, pois são percorridos mais frequentemente.

### Componentes Principais do Algoritmo

1. **Feromônio (τ)**
   - Representa a "memória" do sistema
   - É depositado nas arestas entre as cidades
   - Influencia a escolha do caminho das formigas
   - Evapora ao longo do tempo para evitar convergência prematura

2. **Informação Heurística (η)**
   - Baseada na distância entre as cidades
   - η = 1/d, onde d é a distância
   - Representa a "visibilidade" ou atratividade local

3. **Regra de Transição**
   A probabilidade de uma formiga k escolher ir da cidade i para a cidade j é dada por:

   \[p_{ij}^k = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{l \in N_i^k} [\tau_{il}]^\alpha \cdot [\eta_{il}]^\beta}\]

   Onde:
   - τij: quantidade de feromônio na aresta (i,j)
   - ηij: valor heurístico da aresta (i,j)
   - α: importância do feromônio (parâmetro)
   - β: importância da informação heurística (parâmetro)
   - Ni^k: conjunto de cidades ainda não visitadas pela formiga k

### Fases do Algoritmo

1. **Inicialização**
   ```python
   # Inicialização dos feromônios com valor constante
   self.pheromone = {(city1, city2): 1 for (city1, city2) in distances.keys()}
   ```

2. **Construção de Soluções**
   ```python
   def ant_tour(self):
       # Cada formiga constrói um caminho completo
       path = [start_city]
       while unvisited:
           next_city = self._select_next_city(current, unvisited)
           path.append(next_city)
   ```

3. **Atualização de Feromônios**
   ```python
   # Evaporação
   for key in self.pheromone:
       self.pheromone[key] *= (1 - self.decay)
   
   # Depósito
   for path, distance in ant_paths:
       amount = 1.0 / distance
       for i in range(len(path)):
           self.pheromone[(path[i], path[i+1])] += amount
   ```

### Parâmetros Importantes

1. **Taxa de Evaporação (ρ)**
   - Controla quanto do feromônio evapora em cada iteração
   - ρ ∈ [0,1]
   - Valores típicos: 0.1 a 0.3
   - Evita convergência prematura

2. **Alpha (α)**
   - Controla a importância do feromônio
   - α > 0
   - Valores típicos: 1 a 2
   - α grande → maior influência do feromônio

3. **Beta (β)**
   - Controla a importância da informação heurística
   - β > 0
   - Valores típicos: 2 a 5
   - β grande → maior influência das distâncias

### Pseudocódigo Detalhado

## Requisitos

- Python 3.x
- Bibliotecas Python:
  ```bash
  pip install numpy matplotlib networkx
  ```

## Estrutura do Projeto 
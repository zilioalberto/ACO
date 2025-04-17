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

## Requisitos

- Python 3.x
- Bibliotecas Python:
  ```bash
  pip install numpy matplotlib networkx
  ```

## Estrutura do Projeto 
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import random
import networkx as nx

class ACO:
    def __init__(self, distances: Dict[Tuple[str, str], int], coordinates: Dict[str, Tuple[float, float]], 
                 n_ants: int = 10, n_iterations: int = 100, decay: float = 0.1, alpha: float = 1, beta: float = 2):
        self.distances = distances
        self.coordinates = coordinates
        self.cities = list(set([city for pair in distances.keys() for city in pair]))
        self.n_cities = len(self.cities)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha  # importância do feromônio
        self.beta = beta    # importância da distância
        
        # Inicializa matriz de feromônios
        self.pheromone = {}
        for (city1, city2), distance in distances.items():
            self.pheromone[(city1, city2)] = 1
            self.pheromone[(city2, city1)] = 1
            
        self.best_path = None
        self.best_distance = float('inf')
        self.history = []

    def get_distance(self, city1: str, city2: str) -> int:
        if (city1, city2) in self.distances:
            return self.distances[(city1, city2)]
        return self.distances[(city2, city1)]

    def ant_tour(self) -> Tuple[List[str], float]:
        unvisited = self.cities.copy()
        start = random.choice(unvisited)
        path = [start]
        unvisited.remove(start)
        total_distance = 0

        current = start
        while unvisited:
            next_city = self._select_next_city(current, unvisited)
            path.append(next_city)
            total_distance += self.get_distance(current, next_city)
            unvisited.remove(next_city)
            current = next_city

        # Retorna ao início
        total_distance += self.get_distance(path[-1], path[0])
        return path, total_distance

    def _select_next_city(self, current: str, unvisited: List[str]) -> str:
        probabilities = []
        for city in unvisited:
            # Calcula a probabilidade usando feromônio e distância
            pheromone = self.pheromone.get((current, city), 
                                         self.pheromone.get((city, current)))
            distance = self.get_distance(current, city)
            probability = (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta)
            probabilities.append((city, probability))

        # Normaliza as probabilidades
        total = sum(prob for _, prob in probabilities)
        probabilities = [(city, prob/total) for city, prob in probabilities]
        
        # Seleciona a próxima cidade usando roleta
        r = random.random()
        cumsum = 0
        for city, prob in probabilities:
            cumsum += prob
            if r <= cumsum:
                return city
        return probabilities[-1][0]

    def run(self) -> Tuple[List[str], float]:
        for iteration in range(self.n_iterations):
            # Coleta os caminhos de todas as formigas
            ant_paths = []
            for _ in range(self.n_ants):
                path, distance = self.ant_tour()
                ant_paths.append((path, distance))
                
                # Atualiza o melhor caminho global
                if distance < self.best_distance:
                    self.best_path = path
                    self.best_distance = distance
            
            self.history.append(self.best_distance)
            
            # Evapora os feromônios
            for key in self.pheromone:
                self.pheromone[key] *= (1 - self.decay)
            
            # Adiciona novos feromônios
            for path, distance in ant_paths:
                amount = 1.0 / distance
                for i in range(len(path)):
                    city1 = path[i]
                    city2 = path[(i + 1) % len(path)]
                    self.pheromone[(city1, city2)] += amount
                    self.pheromone[(city2, city1)] += amount

        return self.best_path, self.best_distance

 
    def plot_solution(self):
        plt.figure(figsize=(10, 10))
        
        # Plota as cidades
        x = [self.coordinates[city][0] for city in self.cities]
        y = [self.coordinates[city][1] for city in self.cities]
        plt.scatter(x, y, c='red', s=200)
        
        # Adiciona labels das cidades
        for city in self.cities:
            plt.annotate(city, (self.coordinates[city][0], self.coordinates[city][1]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=12)
        
        # Plota todas as conexões possíveis em cinza claro
        for (city1, city2) in self.distances.keys():
            x1, y1 = self.coordinates[city1]
            x2, y2 = self.coordinates[city2]
            plt.plot([x1, x2], [y1, y2], 'lightgray', linestyle='--', alpha=0.5)
            # Adiciona a distância no meio da linha
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            plt.annotate(str(self.distances[(city1, city2)]), 
                        (mid_x, mid_y), fontsize=10, 
                        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        # Plota o melhor caminho encontrado
        if self.best_path:
            for i in range(len(self.best_path)):
                city1 = self.best_path[i]
                city2 = self.best_path[(i + 1) % len(self.best_path)]
                x1, y1 = self.coordinates[city1]
                x2, y2 = self.coordinates[city2]
                plt.plot([x1, x2], [y1, y2], 'b-', linewidth=2)

        plt.title('Solução do Caixeiro Viajante\n' + 
                 f"Melhor caminho: {' -> '.join(self.best_path + [self.best_path[0]])}\n" +
                 f"Distância total: {self.best_distance}")
        plt.grid(True)
        plt.axis('equal')
        plt.show()

# Exemplo de uso
if __name__ == "__main__":
    # Definição das distâncias entre as cidades
    distances = {
        ('A', 'B'): 10,
        ('A', 'C'): 15,
        ('A', 'D'): 20,
        ('B', 'C'): 35,
        ('B', 'D'): 25,
        ('C', 'D'): 30
    }

    # Definição das coordenadas das cidades (para visualização)
    coordinates = {
        'A': (0, 0),    # Cidade A na origem
        'B': (10, 0),   # Cidade B à direita de A
        'C': (5, 10),   # Cidade C acima e entre A e B
        'D': (15, 5)    # Cidade D à direita e acima de B
    }

    # Criação e execução do ACO
    aco = ACO(distances, coordinates, n_ants=10, n_iterations=100, decay=0.1, alpha=1, beta=2)
    best_path, best_distance = aco.run()

    print(f"Melhor caminho encontrado: {' -> '.join(best_path + [best_path[0]])}")
    print(f"Distância total: {best_distance}")

    # Plotar os gráficos

    aco.plot_solution() 
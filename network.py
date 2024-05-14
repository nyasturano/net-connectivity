import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import itertools
from node import Node


def distance(node1, node2):
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def random_in_radius(center, radius):
    angle = np.random.uniform(0, 2 * np.pi)
    r = np.random.uniform(0, radius)
    return center[0] + r * np.cos(angle), center[1] + r * np.sin(angle)


class Network:
    def __init__(self, area_width, area_height, radius, nodes_count, steps):

        center = (area_width / 2, area_height / 2)

        self.key_mode = False
        self.control_mode = False
        self.debug_mode = False

        self.area_width = area_width
        self.area_height = area_height
        self.radius = radius
        self.steps = steps

        self.G = nx.Graph()
        self.G.add_nodes_from([Node(*random_in_radius(center, radius))
                               for _ in range(nodes_count)])

        self.G_next = nx.Graph()
        self.G_next.add_nodes_from([Node(node.x, node.y, origin=node) for node in self.G.nodes()])

        self.connectivity_history = []

        self.managed_vectors = {}
        self.managed_sums = {}

        for node in self.G.nodes:
            self.managed_vectors[node] = np.array([0.0, 0.0])
            self.managed_sums[node] = 0.0

    def step(self, ax, control_mode=True):
        self.move_nodes()
        self.update_edges(self.G)

        self.find_critical_nodes()

        if self.control_mode:
            self.manage_critical_nodes()

        if self.debug_mode:
            self.draw(ax)

    def find_critical_nodes(self):
        # отмечаем все узлы, как некритические
        for node in self.G.nodes:
            node.is_critical = False

        # симулируем состояние сети на следующий момент времени (G_next)
        for node in self.G_next.nodes:
            node.simulate_from_origin()

        self.update_edges(self.G_next)

        # раскрашиваем компоненты связности графа G в разные цвета
        components = list(nx.connected_components(self.G_next))
        num_of_components = len(components)

        if num_of_components > 1:
            current_color = 0
            for component in components:
                for node in component:
                    node.origin.color = current_color
                current_color += 1

            # если отсутствует ребро между компонентами связности, то узлы критические
            for edge in self.G.edges():
                n1, n2 = edge
                if n1.color != n2.color:
                    n1.is_critical = True
                    n2.is_critical = True

                    v = np.array([n2.x - n1.x, n2.y - n1.y])
                    v_norm = np.linalg.norm(v)

                    # расчеты для интерполяции
                    self.managed_vectors[n1] += v * v_norm
                    self.managed_vectors[n2] += -v * v_norm

                    self.managed_sums[n1] += v_norm
                    self.managed_sums[n2] += v_norm

        # обновляем статистику
        self.connectivity_history.append(nx.number_connected_components(self.G))

    def manage_critical_nodes(self):
        for node in self.G.nodes:
            if node.is_critical:
                v = self.managed_vectors[node] / self.managed_sums[node]
                node.manage(direction=(v[0], v[1]))

    def move_nodes(self):
        for node in self.G.nodes:
            node.update()

    def update_edges(self, graph):
        node_pairs = list(itertools.combinations(graph.nodes(), 2))
        for pair in node_pairs:
            n1, n2 = pair
            if distance(n1, n2) < self.radius:
                if not graph.has_edge(n1, n2):
                    graph.add_edge(n1, n2)
            else:
                if graph.has_edge(n1, n2):
                    graph.remove_edge(n1, n2)

    def draw(self, ax):
        ax.clear()
        ax.set_title('С управлением' if self.control_mode else 'Без управления')
        ax.set_xlim(0, self.area_width)
        ax.set_ylim(0, self.area_height)

        colors = ['red' if node.is_critical else 'blue' for node in self.G.nodes()]

        # отрисовка симуляции
        # if self.debug_mode:
        #     pos = {node: (node.x, node.y) for node in self.G_next.nodes}
        #     nx.draw(self.G_next, pos=pos, ax=ax, node_size=50, with_labels=False, edge_color='grey', alpha=0.4)

        pos = {node: (node.x, node.y) for node in self.G.nodes}
        nx.draw(self.G, pos=pos, ax=ax, node_size=50, with_labels=False, edge_color='gray', node_color=colors)

        plt.draw()
        if self.key_mode:
            plt.waitforbuttonpress()
        else:
            plt.pause(0.001)

    def start(self, control_mode=False, key_mode=False, debug_mode=False):
        self.debug_mode = debug_mode
        self.key_mode = key_mode
        self.control_mode = control_mode

        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))

        for step in range(self.steps):
            self.step(ax)

        plt.ioff()
        plt.show()

        plt.title("Статистика связности сети")
        plt.plot(range(self.steps), self.connectivity_history)
        plt.xlabel("Время")
        plt.ylabel("Кол-во компонент связности")
        plt.show()

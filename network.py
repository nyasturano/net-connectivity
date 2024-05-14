import itertools

import numpy as np
from net_node import Node

import networkx as nx
import matplotlib.pyplot as plt


def distance(node1, node2):
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def random_in_radius(center, radius):
    angle = np.random.uniform(0, 2 * np.pi)
    r = np.random.uniform(0, radius)
    return center[0] + r * np.cos(angle), center[1] + r * np.sin(angle)


VELOCITY_MULTIPLIER = 5


class Network:
    def __init__(self, area_width, area_height, radius, nodes_count, steps):
        center = (area_width / 2, area_height / 2)

        self.area_width = area_width
        self.area_height = area_height
        self.radius = radius
        self.steps = steps

        self.G = nx.Graph()
        self.G.add_nodes_from([Node(*random_in_radius(center, radius))
                               for _ in range(nodes_count)])

        self.connectivity_history = []

    def step(self, ax):
        ax.clear()
        ax.set_xlim(0, self.area_width)
        ax.set_ylim(0, self.area_height)

        self.move_nodes()
        self.update_edges()

        self.critical_nodes(ax)

        self.draw(ax)

        self.connectivity_history.append(nx.number_connected_components(self.G))

        plt.draw()
        plt.waitforbuttonpress()

    def critical_nodes(self, ax):
        # симулируем состояние сети на следующий момент времени
        # отмечаем все узлы, как некритические
        for node in self.G.nodes:
            node.is_critical = False
            node.simulate_update(VELOCITY_MULTIPLIER, self.area_width, self.area_height)

        self.update_edges()

        # раскрашиваем компоненты связности графа в разные цвета
        components = nx.connected_components(self.G)
        color = 0
        for component in components:
            for node in component:
                node.color = color
            color += 1

        # отрисовка симуляции
        # pos = {node: (node.x, node.y) for node in self.G.nodes}
        # nx.draw(self.G, pos=pos, ax=ax, node_size=50, with_labels=False, edge_color='grey', alpha=0.4)

        # возвращаем сеть в исходное состояние
        for node in self.G.nodes:
            node.revert()

        self.update_edges()

        for edge in self.G.edges():
            n1, n2 = edge
            if n1.color != n2.color:
                n1.is_critical = True
                n2.is_critical = True

        self.manage_critical_nodes()

    def manage_critical_nodes(self):

        for node in self.G.nodes:
            if node.is_critical:
                neighbours = self.G.neighbors(node)
                c_n = []

                for n in neighbours:
                    if n.is_critical:
                        c_n.append(n)

                # линейная интерполяция
                s = 0
                result = (0, 0)

                for n in c_n:
                    v = (n.x - node.x, n.y - node.y)
                    len = np.sqrt(v[0] ** 2 + v[1] ** 2)
                    result = (v[0] * len, v[1] * len)
                    s += len

                result = (result[0] / s, result[1] / s)

                node.manage_update(direction=(result[0], result[1]))

    def move_nodes(self):
        for node in self.G.nodes:
            node.update(self.area_width, self.area_height)

    def update_edges(self):
        node_pairs = list(itertools.combinations(self.G.nodes(), 2))
        for pair in node_pairs:
            n1, n2 = pair
            if distance(n1, n2) < self.radius:
                if not self.G.has_edge(n1, n2):
                    self.G.add_edge(n1, n2)
            else:
                if self.G.has_edge(n1, n2):
                    self.G.remove_edge(n1, n2)

    def draw(self, ax):
        colors = ['red' if node.is_critical else 'blue' for node in self.G.nodes()]

        pos = {node: (node.x, node.y) for node in self.G.nodes}
        nx.draw(self.G, pos=pos, ax=ax, node_size=50, with_labels=False, edge_color='gray', node_color=colors)

    def start(self):
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title('Поведение сети')

        for step in range(self.steps):
            self.step(ax)
            self.draw(ax)

        plt.ioff()
        plt.show()

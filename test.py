import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Параметры сети
AREA_WIDTH = 100
AREA_HEIGHT = 100
RADIUS = 10
N_NODES = 50

# Генерация начальных координат узлов
nodes = [{'x': np.random.uniform(0, AREA_WIDTH), 'y': np.random.uniform(0, AREA_HEIGHT)} for _ in range(N_NODES)]


def move_nodes(nodes):
    for node in nodes:
        node['x'] += np.random.uniform(-1, 1)
        node['y'] += np.random.uniform(-1, 1)


def connectivity(nodes):
    G = nx.Graph()
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes[i + 1:], start=i + 1):
            dist = np.sqrt((node1['x'] - node2['x']) ** 2 + (node1['y'] - node2['y']) ** 2)
            if dist < RADIUS:
                G.add_edge(i, j)
    return nx.is_connected(G)


def critical_nodes(nodes, prev_nodes, threshold):
    critical = []
    for i, node1 in enumerate(nodes):
        prev_node = prev_nodes[i]
        dist = np.sqrt((node1['x'] - prev_node['x']) ** 2 + (node1['y'] - prev_node['y']) ** 2)
        if dist > threshold:
            critical.append(i)
    return critical


def plot_network(nodes, ax):
    ax.clear()  # Очищаем оси перед построением нового графика
    ax.set_xlim(0, AREA_WIDTH)
    ax.set_ylim(0, AREA_HEIGHT)

    for node in nodes:
        ax.plot(node['x'], node['y'], 'bo', markersize=5)  # Узлы синими точками

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Network Nodes')
    ax.grid(True)
    plt.draw()
    plt.pause(0.001)  # Пауза для обновления рисунка


# Включаем интерактивный режим
plt.ion()

# Создаем окно для графика
fig, ax = plt.subplots(figsize=(8, 6))

# Симуляция и визуализация
n_steps = 100
connectivity_history = []
for step in range(n_steps):
    move_nodes(nodes)
    connectivity_history.append(connectivity(nodes))
    # critical = critical_nodes(nodes)
    # manage_critical_nodes(nodes, critical)
    plot_network(nodes, ax)

# Выключаем интерактивный режим после завершения симуляции
plt.ioff()
plt.show()

plt.ion()
fig, ax = plt.subplots(figsize=(8, 6))

# Сохраняем предыдущие координаты узлов
prev_nodes = [{'x': node['x'], 'y': node['y']} for node in nodes]

n_steps = 100
connectivity_history = []
for step in range(n_steps):
    move_nodes(nodes)
    connectivity_history.append(connectivity(nodes))

    # Определяем критические узлы на основе изменений координат
    threshold = 1.0  # Порог расстояния
    critical = critical_nodes(nodes, prev_nodes, threshold)

    # Обновляем предыдущие координаты узлов
    prev_nodes = [{'x': node['x'], 'y': node['y']} for node in nodes]

    plot_network(nodes, ax, critical)

plt.ioff()
plt.show()

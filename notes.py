import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Параметры модели
N_NODES = 50  # Количество узлов
AREA_WIDTH = 100  # Ширина области
AREA_HEIGHT = 100  # Высота области
RADIUS = 10  # Радиус связи
MAX_SPEED = 1  # Максимальная скорость
TIME_STEP = 1  # Шаг времени

# Инициализация узлов
nodes = [{'x': np.random.uniform(0, AREA_WIDTH), 'y': np.random.uniform(0, AREA_HEIGHT),
          'vx': np.random.uniform(-MAX_SPEED, MAX_SPEED), 'vy': np.random.uniform(-MAX_SPEED, MAX_SPEED)}
         for _ in range(N_NODES)]


def move_nodes(nodes):
    for node in nodes:
        # Случайное блуждание
        node['x'] += node['vx'] * TIME_STEP
        node['y'] += node['vy'] * TIME_STEP

        # Проверка столкновения с границами области
        if node['x'] < 0 or node['x'] > AREA_WIDTH:
            node['vx'] *= -1
        if node['y'] < 0 or node['y'] > AREA_HEIGHT:
            node['vy'] *= -1


def connectivity(nodes):
    G = nx.Graph()
    for i, node1 in enumerate(nodes):
        G.add_node(i)
        for j, node2 in enumerate(nodes[i + 1:], start=i + 1):
            dist = np.sqrt((node1['x'] - node2['x']) ** 2 + (node1['y'] - node2['y']) ** 2)
            if dist < RADIUS:
                G.add_edge(i, j)
    return nx.number_connected_components(G)


def critical_nodes(nodes):
    critical = []
    for i, node1 in enumerate(nodes):
        # Проверяем, находится ли узел на границе области
        if node1['x'] < RADIUS or node1['x'] > AREA_WIDTH - RADIUS or \
                node1['y'] < RADIUS or node1['y'] > AREA_HEIGHT - RADIUS:
            critical.append(i)
            continue  # Пропускаем узлы на границе области для оценки соседей

        num_neighbors = 0
        for j, node2 in enumerate(nodes):
            if i != j:
                dist = np.sqrt((node1['x'] - node2['x']) ** 2 + (node1['y'] - node2['y']) ** 2)
                if dist < RADIUS:
                    num_neighbors += 1

        # Проверяем количество соседей
        if num_neighbors == 0:
            critical.append(i)

    return critical


def manage_critical_nodes(nodes, critical_nodes):
    for node_id in critical_nodes:
        nodes[node_id]['vx'] += np.random.uniform(-0.1, 0.1)
        nodes[node_id]['vy'] += np.random.uniform(-0.1, 0.1)
        # Ограничиваем максимальную скорость
        nodes[node_id]['vx'] = np.clip(nodes[node_id]['vx'], -MAX_SPEED, MAX_SPEED)
        nodes[node_id]['vy'] = np.clip(nodes[node_id]['vy'], -MAX_SPEED, MAX_SPEED)


def plot_network(nodes, ax, critical_nodes):
    ax.clear()  # Очищаем оси перед построением нового графика
    ax.set_xlim(0, AREA_WIDTH)
    ax.set_ylim(0, AREA_HEIGHT)

    # Отображаем узлы
    for node in nodes:
        ax.plot(node['x'], node['y'], 'bo', markersize=5)  # Узлы синими точками

    # Отображаем критические узлы красным цветом
    for node_id in critical_nodes:
        ax.plot(nodes[node_id]['x'], nodes[node_id]['y'], 'ro', markersize=5)  # Критические узлы красными точками

    # Создаем граф с помощью networkx
    G = nx.Graph()
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes[i + 1:], start=i + 1):
            dist = np.sqrt((node1['x'] - node2['x']) ** 2 + (node1['y'] - node2['y']) ** 2)
            if dist < RADIUS:
                G.add_edge(i, j)

    # Отображаем ребра
    pos = {i: (nodes[i]['x'], nodes[i]['y']) for i in range(len(nodes))}
    nx.draw(G, pos=pos, ax=ax, node_size=0, with_labels=False, edge_color='gray')

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
    critical = critical_nodes(nodes)
    manage_critical_nodes(nodes, critical)
    plot_network(nodes, ax, critical)

# Выключаем интерактивный режим после завершения симуляции
plt.ioff()
plt.show()

# Визуализация результатов
plt.plot(range(n_steps), connectivity_history)
plt.xlabel('Time Step')
plt.ylabel('Number of Connected Components')
plt.title('Connectivity over Time')
plt.show()

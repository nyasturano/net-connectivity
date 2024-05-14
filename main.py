from network import Network

AREA_WIDTH = 100
AREA_HEIGHT = 100
RADIUS = 10
NODES_COUNT = 50
STEPS = 100

network_without_control = Network(
    AREA_WIDTH,
    AREA_HEIGHT,
    RADIUS,
    NODES_COUNT,
    STEPS)

network_with_control = Network(
    AREA_WIDTH,
    AREA_HEIGHT,
    RADIUS,
    NODES_COUNT,
    STEPS)

# network_without_control.start(debug_mode=True, key_mode=False, control_mode=False)
network_with_control.start(debug_mode=True, key_mode=False, control_mode=True)


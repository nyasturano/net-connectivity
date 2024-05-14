from network import Network

AREA_WIDTH = 100
AREA_HEIGHT = 100
RADIUS = 10
NODES_COUNT = 50
STEPS = 500
KEY_MODE = False

network = Network(
    AREA_WIDTH,
    AREA_HEIGHT,
    RADIUS,
    NODES_COUNT,
    STEPS,
    KEY_MODE)

network.start(debug_mode=False)


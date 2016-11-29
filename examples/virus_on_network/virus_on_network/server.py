from mesa.visualization.modules import Network
from mesa.visualization.ModularVisualization import ModularServer

from virus_on_network.model import VirusModel

count = 0


def portrayal(agent):
    """ This is how agents are displayed. """

    if agent is None:
        return

    portrayal = {"color": "#999999"}
    if agent['infected']:
        portrayal["color"] = "#C70039"

    return portrayal


width = 900
height = 700
num_agents = 100
avg_node_degree = 4
initial_outbreak_size = 10

network = Network(portrayal, width, height)

server = ModularServer(VirusModel, [network], "Network Example",
                       num_agents, width, height,
                       avg_node_degree, initial_outbreak_size)

server.max_steps = 0

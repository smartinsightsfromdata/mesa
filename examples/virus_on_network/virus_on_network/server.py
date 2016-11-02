from mesa.visualization.modules import Network
from mesa.visualization.ModularVisualization import ModularServer

from virus_on_network.model import VirusModel

count = 0


def portrayal(agent):
    """ This is how agents are displayed. """
    print('here')

    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true"}

    if agent:
        portrayal["Color"] = "red"
    else:
        portrayal["Color"] = "grey"

    return portrayal


width = 900
height = 700
num_agents = 100

network = Network(portrayal, width, height)
server = ModularServer(VirusModel, [network], "Network Example",
                       num_agents, width, height)

server.max_steps = 0
server.port = 8888

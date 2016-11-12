import networkx as nx

from decimal import Decimal
from random import choice

from mesa import Agent, Model
from mesa.time import RandomActivation


class VirusAgent(Agent):
    """ A virus agent, which can be infected or not infected. """

    def __init__(self, unique_id, infected=0):
        self.unique_id = unique_id
        self.infected = infected

    def __str__(self):
        return "%s, %s" % (str(self.unique_id), self.infected)


class VirusModel(Model):
    """A virus model with some number of agents"""

    def __init__(self, N=150, width=500, height=500, avg_node_degree=3,
                 initial_outbreak_size=10,):

        self.num_agents = N
        self.avg_node_degree = Decimal(avg_node_degree)
        self.schedule = RandomActivation(self)
        self.graph = self._create_graph()

        self.initial_outbreak_size = initial_outbreak_size
        self.graph = self._infect_nodes(self.initial_outbreak_size)

        self.running = True

    def _create_graph(self):
        """ Initialize graph suring the setup process. """

        G = nx.Graph()

        num_links = round(self.avg_node_degree * self.num_agents / 2)
        # G = nx.dense_gnm_random_graph(self.num_agents, num_links)
        G = nx.erdos_renyi_graph(self.num_agents, num_links)

        # Assign agents to the nodes in the graph
        for i in G.nodes():
            G.node[i]['agent'] = VirusAgent(i).__dict__

            # self.schedule.add(agent)

        return G

    def _infect_nodes(self, N):
        """ Infect nodes according to the initial outbreak size. """

        G = self.graph
        print(N)
        for i in range(N):
            node = choice(G.nodes())

            G.node[node]['agent']['infected'] = 1
            print(G.node[node])
        print(G)
        return G

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

import random
import geojson
from mesa import Model
from mesa.kits.geo import GeoAgent
from mesa.time import RandomActivation
from mesa.kits.geo import GeoSpace
from mesa.datacollection import DataCollector


class SchellingAgent(GeoAgent):
    '''
    Schelling segregation agent
    '''
    def __init__(self, unique_id, model, agent_type, shape, pos):
        '''
         Create a new Schelling agent.

         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        '''
        super().__init__(unique_id, model, shape)
        self.pos = pos
        self.atype = agent_type

    def step(self):
        similar = 0
        different = 0
        neighbors = self.model.grid.get_neighbors(self)
        if neighbors:
            for neighbor in neighbors:
                if neighbor.atype == self.atype:
                    similar += 1
                else:
                    different += 1

        # If unhappy, move:
        if similar < different:
            # Get a list of all empty patches
            empties = [p for p in self.model.grid.patches if p.empty is True]
            # Get the old patch and make it empty again
            old_patch = self.model.grid.patches_at(self.pos)[0]
            old_patch.empty = True
            # Select an empty patch and move there and adopt its shape
            new_patch = random.choice(empties)
            self.shape = new_patch.shape
            self.pos = new_patch.pos
            new_patch.empty = False
        else:
            self.model.happy += 1


class SchellingModel(Model):
    '''
    Model class for the Schelling segregation model.
    '''

    def __init__(self, density, minority_pc):
        '''
        '''
        self.density = density
        self.minority_pc = minority_pc

        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()

        self.happy = 0
        self.datacollector = DataCollector(
            {"happy": lambda m: m.happy})  # Model-level count of happy agents

        self.running = True

        # Set up the grid with patches for every NUTS region
        regions = geojson.load(open('nuts_rg_60M_2013_lvl_2.geojson'))
        self.grid.create_patches(regions)
        for patch in self.grid.patches:
            (x, y) = patch.shape.representative_point().coords.xy
            patch.pos = [x[0], y[0]]
            patch.empty = True

        # Set up agents
        for unique_id, patch in enumerate(self.grid.patches):
            if random.random() < self.density:
                if random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0
                # Use the shape of the patch underneath the agent
                agent = SchellingAgent(unique_id, self, agent_type,
                                       patch.shape, patch.pos)
                self.grid.add_agent(agent)
                self.schedule.add(agent)
                patch.empty = False

        # Update the bounding box of the grid
        self.grid.update_bbox()

    def step(self):
        '''
        Run one step of the model. If All agents are happy, halt the model.
        '''
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False

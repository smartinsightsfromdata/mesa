# -*- coding: utf-8 -*-
"""
The model class for Mesa framework.

Core Objects: Model

"""
import datetime as dt
import random


class Model:
    """ Base class for models. """
    def __init__(self, seed=None):
        """ Create a new model. Overload this method with the actual code to
        start the model.

        Args:
            seed: seed for the random number generator

        Attributes:
            schedule: schedule object
            running: a bool indicating if the model should continue running

        """
        if seed is None:
            self.seed = dt.datetime.now()
        else:
            self.seed = seed
        random.seed(seed)
        self.running = True
        self.schedule = None

    def run_model(self):
        """ Run the model until the end condition is reached. Overload as
        needed.

        """
        while self.running:
            self.step()

    def step(self):
        """ A single step. Fill in here. """
        pass

    def add_agent(self, agent, pos='random', schedule=True):
        """ Add an agent to the model and possibly adds it to the grid and the
        scheduler. Possible Arguments:

        agent: Agent to be added to the model
        pos: The position of the model. Only used if the model has a grid
        If "random" is passed, place the agent at random position. Explicitly
        pass "pos=None" if you want to add an agent without a position
        schedule: True/False. If True add the agent to the models schedule
        """
        agent.model = self
        if self.grid:
            if pos == 'random':
                x = random.randint(0, self.grid.width)
                y = random.randint(0, self.grid.height)
                pos = (x, y)
            self.grid.place_agent(pos)
        if schedule:
            self.schedule.add(agent)

    def remove_agent(self, agent):
        """ Remove an agent from the model, the grid and its scheduler
        """
        agent.model = None
        if agent in self.schedule.agents:
            self.schedule.remove(agent)
        if self.grid:
            self.grid.remove_agent(agent)

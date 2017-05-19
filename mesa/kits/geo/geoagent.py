# -*- coding: utf-8 -*-
from mesa import Agent
from shapely.geometry import mapping
"""
The agent class for Mesa framework.

Core Objects: Agent

"""


class GeoAgent(Agent):
    """ Base class for a geo model agent. """
    def __init__(self, unique_id, model, shape):
        """ Create a new agent. """
        self.unique_id = unique_id
        self.model = model
        self.shape = shape

    def step(self):
        """ A single step of the agent. """
        pass

    def __geo_interface__(self):
        """ Returns a GeoJSON Feature """
        props = dict(vars(self))
        try:
            del props['shape']
            del props['model']
            del props['grid']
        except KeyError:
            pass

        return {'type': 'Feature',
                'geometry': mapping(self.shape),
                'properties': props}

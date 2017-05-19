# -*- coding: utf-8 -*-
from shapely.geometry import mapping
"""
The patch class for Mesa framework.

Core Objects: Patch

"""


class Patch:
    """ Base class for a model patch. """
    def __init__(self, grid):
        """ Create a new agent. """
        self.grid = grid

    def step(self):
        """ A single step of the patch. """
        pass

    def __geo_interface__(self):
        props = dict(vars(self))
        try:
            del props['grid']
            del props['shape']
            del props['model']
        except KeyError:
            pass

        return {'type': 'Feature',
                'geometry': mapping(self.shape),
                'properties': props}

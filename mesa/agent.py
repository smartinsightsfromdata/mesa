# -*- coding: utf-8 -*-
"""
The agent class for Mesa framework.

Core Objects: Agent

"""


class Agent:
    """ Base class for a model agent. """
    def __init__(self, unique_id, model):
        """ Create a new agent. """
        self.unique_id = unique_id
        self.model = model

    def step(self):
        """ A single step of the agent. """
        pass

    def move_agent(self, pos):
        """
        Move agent from its current position to a new position.

        Args:
            pos: Tuple of new position to move the agent to.

        """
        self.grid.move_agent(self, pos)

    def move_to_empty(self, agent):
        """ Moves agent to a random empty cell. """
        self.model.grid.move_to_empty(self)

    def get_neighborhood(self, moore, include_center=False, radius=1):
        """ Return a list of cells that are in the neighborhood of a
        certain point.

        Args:
            moore: If True, return Moore neighborhood
                        (including diagonals)
                   If False, return Von Neumann neighborhood
                        (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of coordinate tuples representing the neighborhood. For
            example with radius 1, it will return list with number of elements
            equals at most 9 (8) if Moore, 5 (4) if Von Neumann (if not
            including the center).

        """
        return self.model.grid.get_neighborhood(self.pos, moore,
                                                include_center=False,
                                                radius=1)

    def get_neighbors(self, moore, include_center=False, radius=1):
        """ Return a list of neighbors.

        Args:
            moore: If True, return Moore neighborhood
                    (including diagonals)
                   If False, return Von Neumann neighborhood
                     (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).

        """
        return self.model.grid.get_neighbors(self.pos, moore,
                                             include_center=False,
                                             radius=1)

from mesa.kits.geo.patch import Patch
from mesa.kits.geo.shapes import as_shape, Point


class GeoSpace:
    def __init__(self, bbox=None):
        self.grid = []
        self.agents = []
        self.patches = []
        self.bbox = bbox

    def create_patches(self, GeoJSON, patch=Patch):
        """ Create a new patch from GeoJSON.
        TODO: Add patch-arguments for custom Patch classes """
        self._create_objects(GeoJSON, patch, "patch")

    def create_agents(self, GeoJSON, agent):
        """ Create a new agent from GeoJSON.
        TODO: Add agent-arguments for the agent class """
        self._create_objects(GeoJSON, agent, "agent")

    def _create_objects(self, GeoJSON, obj, what):
        """ Create an object (either patch or agent) from GeoJSON
        Uses the GeoJSON properties to set objects attributes
        TODO: Check if attributes already exist and warn the user """
        gj = GeoJSON
        geometries = ["Point", "MultiPoint", "LineString",
                      "MultiLineString", "Polygon", "MultiPolygon"]
        objects = []
        if gj['type'] in geometries:
            new_obj = obj(grid=self)
            new_obj.shape = as_shape(gj)
            objects.append(new_obj)

        if gj['type'] == 'GeometryCollection':
            shapes = as_shape(gj)
            for shape in shapes:
                new_obj = obj(grid=self)
                new_obj.shape = shape
                objects.append(new_obj)

        if gj['type'] == 'Feature':
            shape, attributes = as_shape(gj)
            new_obj = obj(grid=self)
            new_obj.shape = shape
            for key, value in attributes.items():
                setattr(new_obj, key, value)
            objects.append(new_obj)

        if gj['type'] == "FeatureCollection":
            features = as_shape(gj)
            for shape, attributes in zip(*features):
                new_obj = obj(grid=self)
                new_obj.shape = shape
                for key, value in attributes.items():
                    setattr(new_obj, key, value)
                objects.append(new_obj)
        if what == 'patch':
            self.patches.extend(objects)
        elif what == 'agent':
            self.agents.extend(objects)

    def add_patch(self, patch):
        """ Add a patch to GeoSpace """
        if isinstance(patch, Patch):
            if hasattr(patch, "shape"):
                self.patches.append(patch)
            else:
                raise AttributeError("GeoSpace patches must have a shape")
        else:
            raise TypeError("Patch is not a patch instance")

    def update_bbox(self, bbox=None):
        """ Update bounding box of the GeoSpace """
        if bbox:
            self.bbox = bbox
        else:
            patch = self.patches[0]
            x, y = patch.shape.exterior.coords.xy
            lon_min = min(x)
            lat_min = min(y)
            lon_max = max(x)
            lat_max = max(y)

            if len(self.patches) > 1:
                for patch in self.patches[1:]:
                    if patch.shape.geom_type == "MultiPolygon":
                        shapes = [s for s in patch.shape]
                    else:
                        shapes = [patch.shape]
                    for shape in shapes:
                        x, y = shape.exterior.coords.xy
                        if min(x) < lon_min:
                            lon_min = min(x)
                        if max(x) > lon_max:
                            lon_max = max(x)
                        if min(y) < lat_min:
                            lat_min = min(y)
                        if max(y) > lat_max:
                            lat_max = max(y)
                self.bbox = (lon_min, lat_min, lon_max, lat_max)
        self.center = ((self.bbox[0] + self.bbox[2]) / 2,
                       (self.bbox[1] + self.bbox[3]) / 2)

    def add_agent(self, agent):
        """ Add agent to grid
        TODO: Check if it has a shape """
        self.agents.append(agent)

    def get_neighbors(self, obj):
        """ Return list of neighboring agents that intersect with obj """
        neighbors = []
        for agent in self.agents:
            if obj.shape.intersects(agent.shape):
                neighbors.append(agent)
        return neighbors

    def patches_at(self, pos):
        """ Return a list of patches at given pos """
        patches = []
        for patch in self.patches:
            p = Point(pos)
            if p.within(patch.shape):
                patches.append(patch)
        return patches

    def distance(a, b, unit='degrees'):
        """ Return distance of two shapes.
        Currently only returns distance in degrees """
        dist = a.shape.distance(b.shape)
        if unit == 'degrees':
            return dist

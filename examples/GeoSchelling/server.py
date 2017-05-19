from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from model import SchellingModel


class MapModule(VisualizationElement):
    package_includes = ["leaflet.min.js"]
    local_includes = ["Map.js"]

    def __init__(self, view, zoom, map_height, map_width):
        self.map_height = map_height
        self.map_width = map_width
        self.view = view
        new_element = "new MapModule({}, {}, {}, {})"
        new_element = new_element.format(view,
                                         zoom,
                                         map_width,
                                         map_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        agents = [a.__geo_interface__() for a in model.grid.agents]
        patches = [p.__geo_interface__() for p in model.grid.patches]
        return [agents, patches]


class HappyElement(TextElement):
    '''
    Display a text count of how many happy agents there are.
    '''
    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)


def schelling_draw(agent):
    '''
    Portrayal Method for canvas
    '''
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.atype == 0:
        portrayal["Color"] = "Red"
    else:
        portrayal["Color"] = "Blue"
    return portrayal


happy_element = HappyElement()
canvas_element = CanvasGrid(schelling_draw, 20, 20, 500, 500)
map_element = MapModule([52, 12], 4, 500, 500)
happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])
server = ModularServer(SchellingModel,
                       [map_element, happy_element, happy_chart],
                       "Schelling", 0.8, 0.4)
server.launch()

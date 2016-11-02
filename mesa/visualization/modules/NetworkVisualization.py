# -*- coding: utf-8 -*-
"""
Modular Network Rending
========================

Module for visualizing a model object that is a network.

"""
import json
from networkx.readwrite import json_graph
from mesa.visualization.ModularVisualization import VisualizationElement


class Network(VisualizationElement):
    package_includes = ["d3.v4.min.js", "networkdraw.js"]
    # TODO move this to the model
    css_includes = ["virus_on_network/virus_styles.css"]
    portrayal_method = None

    def __init__(self, portrayal, width=600, height=800):

        self.portrayal = portrayal
        self.width = width
        self.height = height

        new_element = "new NetworkModule({}, {})"
        new_element = new_element.format(width, height)

        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        """
            Networkx's json_graph turns graph into dictionary.
            This allows us to pass the graph as a Json.
        """

        data = json_graph.node_link_data(model.graph)
        json_data = json.dumps(data)
        return json_data

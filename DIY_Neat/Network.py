aggregators = ["SUM", "MEAN", "MIN", "MAX", "MID"]
neuron_types = ["INPUT", "OUTPUT", "BIAS", "HIDDEN"]

# Need to keep track of vertices (nodes) and edges (links)

# Edges: Connects two neurons with some weights.
class Link:
    def __init__(self, input, output, weight = 1, enabled = 1):
        self.input = input
        self.output = output
        self.input.outputs.append(self)
        self.output.inputs.append(self)
        self.weight = weight
        self.enabled = enabled

# Vertices: Takes in inputs and gives outputs.
class Neuron:
    def __init__(self, id, type, x, y, aggregator):
        # Keep track of where, what and when.
        self.id = id
        self.type = type
        self.pos_x = x
        self.pos_y = y
        self.aggregator = aggregator
        self.inputs = []
        self.outputs = []
        self.value = 0

# The graph, made of vertices and edges.
class Genome:
    def __init__(self, neurons, links):
        self.neurons = neurons
        self.links = links

    def connect_neurons(self):
        # Start from input layer and go to the output layer.
        for i in range(len(self.neurons)):
            # Input layer has no inputs.
            if (self.neurons.type == "INPUT"):
                continue
            for j in range(len(self.links)):
                # Some links are not enabled.
                if self.links[j].enabled == 0:
                    continue
                if self.links[j].output == self.neurons[i]:
                    self.neurons[i].inputs.append(self.links[j])
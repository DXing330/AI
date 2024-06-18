import math
import json

class Object(object):
    pass

def sigmoid(x):
  return 1/(1 + math.exp(-x))

def sigmoid2(x, response=1/4.924273):
    # response=1/4.924273 to get -1 at x = -1 and 1 at x = 1
    return (1.0 / (1.0 + math.exp(-x/response))) * 2.0 - 1.0

neuron_types = ["INPUT", "OUTPUT", "HIDDEN", "BIAS"]
run_types = ["ACTIVE", "SNAPSHOT"]

# Connects two neurons.
class Link:
   def __init__(self, neurons, link_gen):
        # Probably need to learn about lambda stuff more.
        self.input_neuron = next(filter(lambda n: n.id == link_gen.from_neuron_id, neurons)) # Gets the input neuron somehow.
        self.output_neuron = next(filter(lambda n: n.id == link_gen.to_neuron_id, neurons)) # Gets the output neuron somehow.
        self.input_neuron.outputs.append(self)
        self.output_neuron.inputs.append(self)
        self.weight = link_gen.weight

class Neuron:
    def __init__(self, gen):
        self.id = gen.id
        self.type = gen.type
        self.inputs = []
        self.outputs = []
        self.sum_activation = 0
        self.value = 0
        self.activation_response = gen.activation_response
        self.pos_x = gen.pos_x
        self.pos_y = gen.pos_y

class Network:
    def __init__(self, genome, filename = None):
        self.genotype = genome
        self.filename = filename

        if filename != None:
            # load from file
            import json
            f = open(filename, 'r')
            data = json.loads(f.read())
            f.close()

            self.neurons = []
            splits = set()
            for d in data['neurons']:
                o = Object()
                o.id = d['id']
                o.type = d['type']
                o.activation_response = d['activation_response']
                o.pos_x = d['pos_x']
                o.pos_y = d['pos_y']
                self.neurons.append(Neuron(o))
                splits.add(o.pos_y)
            self.depth = len(splits)

            self.links = []
            for d in data['links']:
                o = Object()
                o.from_neuron_id = d['input_neuron'] # TODO: input_neuron_id
                o.to_neuron_id = d['output_neuron']
                o.weight = d['weight']
                self.links.append(Link(self.neurons, o))

        else:
            self.neurons = []
            splits = set()
            for neuron_gen in genome.neurons:
                self.neurons.append(Neuron(neuron_gen))
                splits.add(neuron_gen.pos_y)
            self.depth = len(splits)

            self.links = []
            for link_gen in genome.links:
                if not link_gen.disabled:
                    self.links.append(Link(self.neurons, link_gen))

    def dump(self, filename):
        data = {'neurons': [], 'links': []}
        for neuron in self.neurons:
            d = {   'id': neuron.id,
                    'type': neuron.type,
                    'value': neuron.value,
                    'activation_response': neuron.activation_response,
                    'pos_x': neuron.pos_x,
                    'pos_y': neuron.pos_y  }
            data['neurons'].append(d)
        for link in self.links:
            d = {   'input_neuron': link.input_neuron.id,
                    'output_neuron': link.output_neuron.id,
                    'weight': link.weight  }
            data['links'].append(d)
        f = open(filename+'.json', 'w')
        f.write(json.dumps(data))
        f.close()

    def feed(self, inputs, run_type="SNAPSHOT"):

        if run_type == "SNAPSHOT":
            flush_count = self.depth
            for neuron in self.neurons:
                neuron.value = 0
        else:
            flush_count = 1

        for i in range(flush_count):
            outputs = []
            i_input = 0
            i_bias = 0
            for neuron in self.neurons:
                if neuron.type == "INPUT":
                    neuron.value = inputs[i_input]
                    i_input += 1
                elif neuron.type == "BIAS":
                    neuron.value = 1
                    i_bias += 1
                else:
                    sum = 0.0
                    for link in neuron.input_links:
                        sum += link.weight * link.input_neuron.value
                    value = sigmoid2(sum, neuron.activation_response)
                    neuron.value = value
                    if neuron.type == "OUTPUT":
                        outputs.append(value)

        return outputs
        #return np.array(outputs)
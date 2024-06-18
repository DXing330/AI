innovation_types = ["NEURON", "LINK"] # NEURON, LINK

class Innovation:
    def __init__(self, innv_id, innv_type, input_id = None, output_id = None, neuron_id = None, link_id = None):
        self.id = innv_id
        self.type = innv_type
        self.input = input_id
        self.output = output_id
        self.neuron = neuron_id
        self.link = link_id

class InnovationDB:
    def __init__(self):
        self.innovations = []
        self.next_innovation_id = 0
        self.next_neuron_id = 0
        self.next_link_id = 0

    def exist_innovation(self, innovation_type, in_neuron_id, out_neuron_id):
        for innovation in self.innovations:
            if innovation.type == innovation_type and innovation.input == in_neuron_id and innovation.output == out_neuron_id:
                return innovation
        return None
    
    def create_innovation(self, innovation_type, in_neuron_id=None, out_neuron_id=None):
        if in_neuron_id == None or out_neuron_id == None:
            return None
        if innovation_type == innovation_types[0]:
            innovation = Innovation(self.next_innovation_id, innovation_type, in_neuron_id, out_neuron_id, neuron_id=self.next_neuron_id)
            self.next_neuron_id += 1
        elif innovation_type == innovation_types[1]:
            innovation = Innovation(self.next_innovation_id, innovation_type, in_neuron_id, out_neuron_id, link_id=self.next_link_id)
            self.next_link_id += 1
        else:
            return None
        self.innovations.append(innovation)
        self.next_innovation_id += 1
        return innovation
    
    def get_innovation(self, innovation_type, in_neuron_id=None, out_neuron_id=None):
        innovation = self.exist_innovation(innovation_type, in_neuron_id, out_neuron_id)
        if innovation == None:
            innovation = self.create_innovation(innovation_type, in_neuron_id, out_neuron_id)
        return innovation
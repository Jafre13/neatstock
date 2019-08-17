import random
import json
import Innovation
class ConnectionGene:
    def __init__(self, input, output, enabled, innovation=None, weight=None):
        self.input = input
        self.output = output
        self.enabled = enabled
        if innovation==None:
            self.innovation=Innovation.getConnectionInnovation()
        else:
            self.innovation = innovation
        if weight == None:
            self.weight = random.random()
        else:
            self.weight = weight
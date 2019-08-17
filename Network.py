from NodeGene import NodeGene
from NodeType import NodeType
from ConnectionGene import ConnectionGene
from Genome import Genome
import numpy as np
import Innovation
import copy
import pprint
import json


class Network:
    def __init__(self, genome, debug=False):
        self.inputs = [n for n in genome.nodes if n.nodeType == NodeType.INPUT]
        self.outputs = [n for n in genome.nodes if n.nodeType == NodeType.OUTPUT]
        self.hidden = [n for n in genome.nodes if n.nodeType == NodeType.HIDDEN]

        self.debug = debug
        self.connections = dict()
        for connection in genome.connections:
            if connection.enabled:
                if connection.output in self.connections:
                    self.connections[connection.output].append(copy.copy(connection))
                else:
                    self.connections[connection.output] = [copy.copy(connection)]

        self.values = {n.number: None for n in genome.nodes}
        self.previousValues = {n.number: 0 for n in genome.nodes}
        self.visitedNodes = []

        if self.debug:
            print(self.previousValues)
            for n in genome.nodes:
                print("Network node: " + json.dumps(n.__dict__))

            for c in self.connections.values():
                for t in c:
                    print("Network connection: " + json.dumps(t.__dict__))

    def run(self, inputs):
        for i in range(0, len(inputs)):
            self.values[self.inputs[i].number] = inputs[i]

        result = dict()
        for output in self.outputs:
            result[output.number] = self.getNodeValue(output.number)
        if self.debug:
            print("network values: " + str(self.values.values()))

        self.housekeeping()
        return result

    def getNodeValue(self, node):
        if self.debug:
            print("Finding result for node: " + str(node))
        result = self.values.get(node)
        if (result == None):
            if node not in self.visitedNodes:
                self.visitedNodes.append(node)
                result = self.getSum(node);
                self.values[node] = result
            else:
                result = self.previousValues.get(node)
                if self.debug:
                    print("Already visited node: " + str(node) + " instead using previous value: " + str(result))
        if self.debug:
            print("Result for node: " + str(node) + " : " + str(result))
        return result

    def getSum(self, node):
        connections = self.connections.get(node)
        result = 0
        if connections != None:
            nodes = ""
            for con in connections:
                nodes += str(con.input) + ", "
                result = result + self.getNodeValue(con.input) * con.weight

            if self.debug:
                print("Finding sum for nodes: " + nodes)
        result = self.sigmoid(result)
        if self.debug:
            print("Sum for node: " + str(node) + " : " + str(result))
        return result

    def sigmoid(self, value):
        return 1 / (1 + np.exp(-value))

    def housekeeping(self):
        self.previousValues = self.values;
        self.values = {n.number: None for n in genome.nodes}
        self.visitedNodes = []


# input = [NodeGene(NodeType.INPUT) for i in range(1, 5)]
# hidden = [NodeGene(NodeType.HIDDEN) for i in range(5, 8)]
# output = [NodeGene(NodeType.OUTPUT) for i in range(9, 11)]
#
# connections = []
# for inNode in input:
#     for hNode in hidden:
#         connections.append(ConnectionGene(inNode.number, hNode.number, True))
#
# for hNode in hidden:
#     for outNode in output:
#         connections.append(ConnectionGene(hNode.number, outNode.number, True))
#
#
# connections.append(ConnectionGene(8,5,True))
#
# nodes = input + hidden + output
#
# genome = Genome(nodes, connections)
#
# # network = Network(genome, debug=False)
# # print("All 1")
# # print(network.run([1,1,1,1]))
# network = Network(genome, debug=True)
# print("All 0")
# print(network.run([0,0,0,0]))
# print(network.run([0,0,0,0]))

# def run2():
inputValues = [1, 1]

input = [NodeGene(NodeType.INPUT) for i in range(1, 3)]
hidden = [NodeGene(NodeType.HIDDEN) for i in range(3, 5)]
output = [NodeGene(NodeType.OUTPUT) for i in range(5, 6)]

connections = []

connections.append(ConnectionGene(1, 3, True))
connections.append(ConnectionGene(2, 3, True))
connections.append(ConnectionGene(2, 4, True))
connections.append(ConnectionGene(3, 4, True))
connections.append(ConnectionGene(4, 5, True))
# Recurring
connections.append(ConnectionGene(3, 3, True))

nodes = input + hidden + output

genome = Genome(nodes, connections)
network = Network(genome, debug=True)
print("All 1")
print(network.run([1, 1]))
print(network.run([1, 1]))

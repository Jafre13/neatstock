import Innovation
class NodeGene:
    def __init__(self, nodeType, number=None):
        if number==None:
            self.number = Innovation.getNodeInnovation()
        else:
            self.number = number
        self.nodeType = nodeType

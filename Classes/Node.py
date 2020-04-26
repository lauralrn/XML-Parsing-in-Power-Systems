from .Terminal import Terminal


class Node:   # A node would be equivalent to an electrical connection

    def __init__(self, nodeNumber, IDCN, nameCN, containerCN):

        self.nodeNumber = nodeNumber
        self.IDCN = IDCN
        self.nameCN = nameCN
        self.containerCN = containerCN
        self.terminalList = [Terminal]

    def addTerminal(self, newTerminal):
        self.terminalList.append(newTerminal)
        # print('Terminal added to node')
        return



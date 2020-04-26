from .Equipment import Equipment

class Terminal:

    def __init__(self, IDTerminal, nameTerminal, CETerminal, CNTerminal):

        self.IDTerminal = IDTerminal
        self.nameTerminal = nameTerminal
        self.CETerminal = CETerminal
        self.CNTerminal = CNTerminal
        self.CEList = [Equipment]

    def addCE(self, newCE):
        self.CEList.append(newCE)
        # print('Conducting Equipment added to node')
        return
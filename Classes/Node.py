class Node:   # A node would be equivalent to an electrical connection

    def __init__(self, ID, name, container):

        self.ID = ID
        self.name = name
        self.container = container
        self.terminalList = []


    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)



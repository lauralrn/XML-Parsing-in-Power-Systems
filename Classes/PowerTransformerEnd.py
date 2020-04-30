class PowerTransformerEnd:

    def __init__(self, ID, name, r, x, IDTransformer, baseVol, terminal, powerTransformer):

        self.ID = ID
        self.name = name
        self.r = r
        self.x = x
        self.IDTransformer = IDTransformer
        self.baseVol = baseVol
        self.terminal = terminal
        self.powerTransformer = powerTransformer
        self.terminalList = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)

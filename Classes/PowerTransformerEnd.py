class PowerTransformerEnd:

    def __init__(self, ID, name, r, x, s, IDTransformer, baseVol, terminal, powerTransformer, end_number):

        self.ID = ID
        self.name = name
        self.r = r
        self.x = x
        self.s = s
        self.IDTransformer = IDTransformer
        self.baseVol = baseVol
        self.terminal = terminal
        self.powerTransformer = powerTransformer
        self.end_number = end_number
        self.terminalList = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)

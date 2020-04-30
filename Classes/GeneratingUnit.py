class GeneratingUnit:

    def __init__(self, ID, name, maxP, minP, power, equipmentCont):
        self.ID = ID
        self.name = name
        self.maxP = maxP
        self.minP = minP
        self.power = power
        self.equipmentCont = equipmentCont
        self.terminalList = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)

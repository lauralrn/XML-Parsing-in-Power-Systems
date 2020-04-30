class EnergyConsumer:

    def __init__(self, ID, name, P, Q, equipmentCont, baseVol):
        self.ID = ID
        self.name = name
        self.P = P
        self.Q = Q
        self.equipmentCont = equipmentCont
        self.baseVol = baseVol
        self.terminalList = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)

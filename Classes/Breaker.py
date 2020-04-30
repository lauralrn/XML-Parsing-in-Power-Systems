class Breaker:

    def __init__(self, ID, name, state, equipmentCont, baseVol):

        self.ID = ID
        self.name = name
        self.state = state
        self.equipmentCont = equipmentCont
        self.baseVol = baseVol
        self.terminalList = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)

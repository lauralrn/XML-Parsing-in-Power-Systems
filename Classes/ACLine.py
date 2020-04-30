class ACLine:

    def __init__(self, ID, name, equipmentCont,lenght, r, x, b, g, baseV):

        self.ID = ID
        self.name = name
        self.equipmentCont = equipmentCont
        self.lenght = lenght
        self.r = r
        self.x = x
        self.b = b
        self.g = g
        self.baseV = baseV
        self.terminalList = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)

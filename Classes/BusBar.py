class BusBar:

    def __init__(self, ID,  name, equipmentCont, voltage):
        self.ID = ID
        self.name = name
        self.equipmentCont = equipmentCont
        self.voltage = voltage
        self.terminalList = []
        self.attached_ce_list = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)
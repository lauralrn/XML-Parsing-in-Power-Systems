class SynchronousMachine:

    def __init__(self, ID, name, rateS, P, Q,gen_unit, regContr, equipmentCont, baseVol):

        self.ID = ID
        self.name = name
        self.rateS = rateS #'RotatingMachine.GeneratingUnit'
        self.P = P
        self.Q = Q
        self.gen_unit =gen_unit
        self.regContr = regContr
        self.equipmentCont = equipmentCont
        self.baseVol = baseVol
        self.terminalList = []

    def add_terminal(self, newTerminal):
        self.terminalList.append(newTerminal)

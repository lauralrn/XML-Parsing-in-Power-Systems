class LinearShuntCompensator:
  def __init__(self,  ID, name,  b, g, equipmentCont, voltage, p, q):
    self.ID = ID
    self.name = name
    self.b = b
    self.g = g
    self.equipmentCont = equipmentCont
    self.voltage= voltage
    self.p = p
    self.q = q
    self.terminalList = []

  def add_terminal(self, newTerminal):
    self.terminalList.append(newTerminal)

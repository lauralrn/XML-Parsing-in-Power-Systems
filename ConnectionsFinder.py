from Classes import LinearShuntCompensator, BusBar
from Classes.Node import Node
from Classes.PowerTransformer import PowerTransformer
from Classes.ACLine import ACLine
from Classes.Terminal import Terminal
from Classes.Breaker import Breaker
from Classes.GeneratingUnit import GeneratingUnit
from Classes.SynchronousMachine import SynchronousMachine
from Classes.EnergyConsumer import EnergyConsumer
from Classes.BusBar import BusBar
from Classes.LinearShuntCompensator import LinearShuntCompensator
from Classes.PowerTransformerEnd import PowerTransformerEnd
#from Main import *




# Add elements in Node class, add them to node_list, find the terminals connected
# and add them to terminalList in node
terminal_list = []
node_list = []
for terminal in microgrid.findall('Terminal'):
    CN = terminal.find('Terminal.ConnectivityNode').attrib['resource']
    ID = terminal.get('ID')
    name = terminal.find('IdentifiedObject.name').text
    CE = terminal.find('Terminal.ConductingEquipment').attrib['resource']
    passed = False
    terminal_class = Terminal(ID, name, CE, CN, passed)
    terminal_list.append(terminal_class)

for node in microgrid.findall('ConnectivityNode'):
    ID = node.get('ID')
    name = node.find('IdentifiedObject.name').text
    container = node.find('ConnectivityNode.ConnectivityNodeContainer').attrib['resource']
    node_class = Node(ID, name, container)

    for terminal in terminal_list:
        if ID == terminal.CN[1:]:
            node_class.add_terminal(terminal)

    node_list.append(node_class)

# Add Conducting Equipment to list
equipment_list = (busbar_list + linear_shunt_compensator_list + generating_unit_list + power_transformer_list +
                  energy_consumer_list + breaker_list + synchronous_machine_list + AC_lines_list)

# Find the terminals connected to every CE and add them to terminalList of each component
for ce in equipment_list:
    if (isinstance(ce, ACLine) or isinstance(ce, Breaker) or isinstance(ce, PowerTransformer)
            or isinstance(ce, SynchronousMachine) or isinstance(ce, LinearShuntCompensator)
            or isinstance(ce, BusBar) or isinstance(ce, EnergyConsumer) or isinstance(ce, PowerTransformerEnd)):
        for terminal in terminal_list:
            if ce.ID == terminal.CE[1:]:
                ce.add_terminal(terminal)

# for the generating unit, at first, the synchronous machine connected to it is found
for ce in generating_unit_list:
    for machine in synchronous_machine_list:
        if ce.ID == machine.gen_unit[1:]:
            ce.terminalList = machine.terminalList

for pt in power_transformer_list:
    pt.terminalList = list(set(pt.terminalList))

# Define function to check if element is a Te
def check_terminal(curr_node):
    return isinstance(curr_node, Terminal)

# Define function to check if element is a CN
def check_CN(curr_node):
    return isinstance(curr_node, Node)

# Define function to check if element is a busbar
def check_busbar(curr_node):
    return isinstance(curr_node, BusBar)

# Define function to check if element is a CE
def check_CE(curr_node):
    return (isinstance(curr_node, ACLine) or isinstance(curr_node, Breaker) or isinstance(curr_node, GeneratingUnit)
            or isinstance(curr_node, PowerTransformer) or isinstance(curr_node, SynchronousMachine)
            or isinstance(curr_node, LinearShuntCompensator) or isinstance(curr_node, BusBar)
            or isinstance(curr_node, EnergyConsumer))

# Define function that finds the node following the input node
def find_next_node(curr_node, prev_node):
    if check_terminal(curr_node):
        if check_CE(prev_node):
            for cn in node_list:
                if cn.ID == curr_node.CN[1:]:
                    next_node = cn
                    return next_node
        if check_CN(prev_node):
            for ce in equipment_list:
                if ce.ID == curr_node.CE[1:]:
                    next_node = ce
                    return next_node
    if check_CN(curr_node):
        for te in terminal_list:
            if curr_node.ID == te.CN[1:]:
                next_node = te
                return next_node
    if check_CE(curr_node):
        for te in curr_node.terminalList:
            if not te.passed:
                next_node = te
                return next_node

# Define function to check if there is a busbar connected to a CN
# Returns the busbar if it is connected to a busbar and false if it is not
def bus_connected_to_CN(CN):
   for terminal in CN.terminalList:
       CE = find_next_node(terminal, CN)
       if isinstance(CE, BusBar):
           return CE
       elif isinstance(CE, Breaker):
           if CE.state == 'false':
               for terminal in CE.terminalList:
                   temp_cn = find_next_node(terminal, CE)
                   for cn_terminal in temp_cn.terminalList:
                       temp_ce = find_next_node(cn_terminal, temp_cn)
                       if isinstance(temp_ce, BusBar):
                           return temp_ce

   return False

# Define function that find the list of CNs of a CE
def find_attached_CN(CE):
    attached_CN_list = []
    for terminal in CE.terminalList:
        CN = find_next_node(terminal, CE)
        attached_CN_list.append(CN)
    return attached_CN_list, CE.terminalList


# Define function that from a CE(!=BusBar) as an input returns the buses attached
def find_attached_busbar(CE):
    if not check_busbar(CE):
        attached_busbar_list = []
        way_terminals_list = []
        conn_node_list, way_terminals = find_attached_CN(CE)
        for cn, wt in zip(conn_node_list, way_terminals):
            # check if the cn is connected to any busbar
            if bus_connected_to_CN(cn) is not False: #if a bus is connected
               bus = bus_connected_to_CN(cn)
               attached_busbar_list.append(bus)
               way_terminals_list.append(wt.ID)
        return attached_busbar_list, way_terminals_list
    return 'current node is already a busbar'


# Define function to find list of CE connected
def find_CE_list(CE):
    CN = find_attached_CN(CE)
    connected_ce_list = []
    for node in CN:
        for te in CN.terminalList:
            connected_ce_list.append(find_next_node(terminal, node))
    return connected_ce_list

#Define function that prints the type of the CE
def ce_type(ce):
    if isinstance(ce, ACLine):
        return 'l'
    if isinstance(ce, Breaker):
        return 'breaker'
    if isinstance(ce, PowerTransformer):
        return 't'
    if isinstance(ce, SynchronousMachine):
        return 's'
    if isinstance(ce, LinearShuntCompensator):
        return 'l'
    if isinstance(ce, EnergyConsumer):
        return 'load'
    if isinstance(ce, BusBar):
        return 'b'





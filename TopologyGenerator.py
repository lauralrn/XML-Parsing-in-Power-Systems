from Classes import LinearShuntCompensator, BusBar
from Classes.Node import Node
from Classes.Substation import Substation
from Classes.BaseVoltage import BaseVoltage
from Classes.VoltageLevel import VoltageLevel
from Classes.PowerTransformer import PowerTransformer
from Classes.ACLine import ACLine
from Classes.Terminal import Terminal
from Classes.Breaker import Breaker
from Classes.GeneratingUnit import GeneratingUnit
from Classes.SynchronousMachine import SynchronousMachine
from Classes.RegulatingControl import RegulatingControl
from Classes.EnergyConsumer import EnergyConsumer
from Classes.BusBar import BusBar
from Classes.LinearShuntCompensator import LinearShuntCompensator
from Classes.PowerTransformerEnd import PowerTransformerEnd
from Classes.RatioTapChanger import RatioTapChanger
from collections import deque


def topology_generator(microgrid, microgrid_SSH, base_voltage_list, busbar_list, linear_shunt_compensator_list,
                       substation_list, voltage_level_list,
                       generating_unit_list, regulating_control_list, power_transformer_list,
                       energy_consumer_list, power_transformer_end_list, breaker_list, ratio_tap_changer_list,
                       synchronous_machine_list, AC_lines_list):
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
                or isinstance(ce, BusBar) or isinstance(ce, EnergyConsumer)):
            for terminal in terminal_list:
                if ce.ID == terminal.CE[1:]:
                    ce.add_terminal(terminal)
    # for the generating unit, at first, the synchronous machine connected to it is found
    for ce in generating_unit_list:
        for machine in synchronous_machine_list:
            if ce.ID == machine.gen_unit[1:]:
                ce.terminalList = machine.terminalList

    # Define function to check if element is a Te
    def check_terminal(curr_node):
        return isinstance(curr_node, Terminal)

    # Define function to check if element is a CN
    def check_CN(curr_node):
        return isinstance(curr_node, Node)



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
                if curr_node.ID == te.CN[1:] and not te.passed:
                    next_node = te
                    return next_node
        if check_CE(curr_node):
            for te in curr_node.terminalList:
                if not te.passed:
                    next_node = te
                    return next_node

    # Define function to check if there is a busbar connected to a CN
    # Returns true is it is connected to a busbar and false if it is not
    def bus_connected_to_CN(CN):
        next_terminal = find_next_node(CN, '')
        if not next_terminal:
            return False
        CE = find_next_node(next_terminal, CN)
        for busbar in busbar_list:
            if CE.ID == busbar.ID:
                return True
        return False

    # Define function that return the bus attached to the terminal, or false if there is none
    def bus_connected_to_te(terminal):
        for busbar in busbar_list:
            if terminal.CE[1:] == busbar.ID:
                return busbar
        return False

    # Define function to find out if in the list of terminals, a terminal il untraversed
    def is_untraversed(node):
        for terminal in node.terminalList:
            if not terminal.passed:
                return True
        return False

    # Define a function that check if CE is a breaker and returns true if terminal is open, false otherwise
    def is_open_breaker(CE):
        for breaker in breaker_list:
            if CE == breaker:
                if breaker.state == 'true':
                    return True
        return False

    # Initialize stacks
    CN_stack = deque(
        [])  # to push a CN as soon as it is visited, pop when all terminals attached to this node are traversed
    CE_stack = deque([])  # to push a CE, as and when encountered
    everything_stack = deque([])  # to push all the visited nodes (CE, CN, Te)

    # Initialize variables to use
    starting_node = generating_unit_list[0]  # Select starting node as an end device
    curr_node = starting_node
    prev_node = 'empty'

    # Get next_node from function and define algorithm
    next_node = find_next_node(curr_node, prev_node)
    final_everything_stack = []
    final_CE_stack = []
    CE_list = []
    bus_flag = False
    flag = False

    while not flag:
        if len(everything_stack) == 0 or curr_node not in everything_stack:
            everything_stack.append(curr_node)   # Add element to everything_stack

        if check_terminal(curr_node): # If curr_node is a terminal
            curr_node.passed = True
            if check_CN(next_node):
                if not bus_connected_to_CN(next_node):  # if CN is not connected to a bus go to next node
                    prev_node = curr_node
                    curr_node = next_node
                    next_node = find_next_node(curr_node, prev_node)
                else:  # if CN is connected to bus, stop the algorithm at the busbar
                    bus_flag = True
                    node_flag = next_node
                    prev_node = curr_node
                    curr_node = next_node
                    next_node = find_next_node(curr_node, prev_node)
            elif check_CE(next_node):
                prev_node = curr_node
                curr_node = next_node
                next_node = find_next_node(curr_node, prev_node)
        # If the current node is a CN
        elif check_CN(curr_node):
            if len(CN_stack) == 0 or curr_node not in  CN_stack:#not CN_stack[-1] == curr_node:
                CN_stack.append(curr_node)  # Push in the CN stack
            if is_untraversed(curr_node):
                prev_node = curr_node
                curr_node = next_node
                next_node = find_next_node(curr_node, prev_node)
            else:  # if there is no untraversed terminal remaining and go to another CN
                final_CE_stack = CE_stack
                #CE_stack = deque([])
                final_everything_stack.append(everything_stack)  # publish the CE_stack and everything_stack
                everything_stack = deque([])
                CN_stack.pop()  # pop the current CN off the CN stack
                if len(CN_stack) != 0:  # if the stack is not empty
                    curr_node = CN_stack[-1]  # mark the next node as the CN on top of CN stack
                    prev_node = 'empty'
                    next_node = find_next_node(curr_node, prev_node)
                else:
                    # final_CE_stack.append(CE_stack)
                    final_CE_stack = CE_stack
                    final_everything_stack.append(everything_stack)  # publish the CE_stack and everything_stack
                    flag = True

        # If the current node is a CE
        elif check_CE(curr_node):
            CE_stack.append(curr_node)  # Push in the CE stack
            if is_untraversed(curr_node) and not is_open_breaker(curr_node):
                prev_node = curr_node
                curr_node = next_node
                next_node = find_next_node(curr_node, prev_node)
            elif (not is_untraversed(curr_node) or is_open_breaker(curr_node)):
                final_CE_stack = CE_stack
                final_everything_stack.append(everything_stack)  # publish the CE_stack, everything_stack
                everything_stack = deque([])
                prev_node = curr_node
                curr_node = CN_stack[-1]  # mark the next node as the CN on top of CN stack
                next_node = find_next_node(curr_node, prev_node)
                if len(CN_stack) == 0:  # if the stack is not empty
                    final_CE_stack = CE_stack
                    final_everything_stack.append(everything_stack)  # publish the CE_stack and everything_stack
                    flag = True
            elif bus_flag:  # go back to the CN
                if not is_untraversed(node_flag):  # if the CN connected to the busbar has no other terminals connected
                    # end the algorithm publish the CE_stack, everything_stack
                    final_CE_stack = CE_stack
                    final_everything_stack.append(everything_stack)
                    everything_stack = deque([])
                    flag = True
                else:  # if the CN has other terminals connected go back
                    curr_node = node_flag  # mark the next node as the CN on top of CN stack
                    prev_node = 'empty'
                    next_node = find_next_node(curr_node, prev_node)
                    bus_flag = False


    #print(curr_node)
    return final_everything_stack, final_CE_stack

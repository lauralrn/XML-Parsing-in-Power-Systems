from Classes.Equipment import Equipment
from Classes.Node import Node
from Classes.Terminal import Terminal

#To develop the algorithm, it is assumed that only three types of nodes will be encountered in the network:
#conducting equipment (class Equipment), connectivity node (class Node) and terminal (class Terminal)

#The Terminal class will contain its ID and type.
#Equipment and Node will have a list of terminals and their number.

#The function (find_next_node) will be used to move from one node to the other and implemented via three traversal node
# objects, representing the previous (prev_node), current (curr_node) and next node (next_node) to be traversed
# respectively.
# when the current traversed node (curr_node) is conducting equipment or a connectivity node,
# the next node will always be a terminal.
# When the current traversed node is a terminal, then the node to be traversed next would be a conducting equipment,
# if the previous node was a connectivity node and vice-versa

#As mentioned before, each conducting equipment and connectivity node in the network will have one or multiple terminals attached to it.
# While traversing a conducting equipment or connectivity node, we need to keep track of all the attached terminals that haven’t been encountered before.
# This is realized by adding an attribute called a ‘traversal flag’ to every terminal in the system with the flag value
# initialized at zero. The traversal flag is set to one once the terminal has been traversed.
# For the purpose of the algorithm, a single terminal conducting equipment will be called an ‘end-device’

def topology_generator(microgrid, microgrid_SSH, base_voltage_list, substation_list, voltage_level_list,
                      generating_unit_list, regulating_control_list, power_transformer_list,
                      energy_consumer_list, power_transformer_end_list, breaker_list, ratio_tap_changer_list,
                      synchronous_machine_list, AC_lines_list):

    # Initialize variables to use
    nodeNumber = 1 #in the GUI it can change
    powerGrid = [Node] #initialize list for Node
    busbarSectionList = []  #initizlize list for buses

    # Step 1: Everytime a connectivity node is encountered, add all the terminal attached to the node
    # Find all Coonectivity Nodes and add to the list
    for node in microgrid .findall('ConnectivityNode'):
        ID  = node. get('ID')
        name  = node. find('IdentifiedObject.name').text
        container  = node. find('ConnectivityNode.ConnectivityNodeContainer').attrib['resource']
        powerGrid.append(Node(nodeNumber, ID, name, container))
        terminal_n = 0 #initialize the number for terminals as zero

        # Find terminals and add them to the connectivity node
        for terminal in microgrid .findall('Terminal'):
            CN = terminal.find('Terminal.ConnectivityNode').attrib['resource']
            if CN[1:] == ID:
                ID = terminal.get('ID')
                name = terminal.find('IdentifiedObject.name').text
                CE = terminal.find('Terminal.ConductingEquipment').attrib['resource']
                powerGrid[nodeNumber].add_terminal(Terminal(ID, name, CE, CN))

                terminal_n += 1 #increase the number of terminals of one

                # Find the Conducting Equipment and add them to the Terminal
                # First, let's look for bus bars

                for bus in microgrid .findall('BusbarSection'):
                    ID = bus.get('ID')
                    if ID == CE[1:]:
                        name = bus.find('IdentifiedObject.name').text
                        equipmentCont = bus.find('Equipment.EquipmentContainer').attrib['resource']
                        busbarSectionList.append(Equipment(ID, name, equipmentCont))
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(Equipment(ID, name, equipmentCont))

                # Now, let's find the Power Transformers

                pos = 0

                for _ in power_transformer_list:
                    ID = power_transformer_list[pos].ID
                    if ID == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(power_transformer_list[pos])
                    pos += 1

                # Now, let's find the Breakers

                pos = 0

                for _ in breaker_list:
                    ID = breaker_list[pos].ID
                    if ID == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(breaker_list[pos])
                    pos += 1

                # Now, let's find the Generation Units

                pos = 0

                for _ in generating_unit_list:
                    ID = generating_unit_list[pos].ID
                    if ID == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(generating_unit_list[pos])
                    pos += 1

                # Now, let's find the Regulating Units

                pos = 0

                for _ in regulating_control_list:
                    ID = regulating_control_list[pos].ID
                    if ID == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(regulating_control_list[pos])
                    pos += 1

                # Are you not getting bored? We find the loads

                pos = 0

                for _ in energy_consumer_list:
                    ID = energy_consumer_list[pos].ID
                    if ID == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(ID[pos])
                    pos += 1

                # Now, we find the Synchronous Machine

                pos = 0

                for _ in synchronous_machine_list:
                    ID = synchronous_machine_list[pos].ID
                    if ID == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(synchronous_machine_list[pos])
                    pos += 1

                # Almost finally... the Power Transformers End

                pos = 0

                for _ in power_transformer_end_list:
                    ID = power_transformer_end_list[pos].ID
                    if ID == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(power_transformer_end_list[pos])
                    pos += 1

                # Finally, the AC Lines

                pos = 0

                for _ in AC_lines_list:
                    IDLine = AC_lines_list[pos].IDLine
                    if IDLine == CE[1:]:
                        powerGrid[nodeNumber].terminalList[terminal_n].addCE(AC_lines_list[pos])
                    pos += 1

        nodeNumber += 1
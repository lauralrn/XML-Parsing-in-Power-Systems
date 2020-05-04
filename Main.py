# Assignment 1  EH2745 Computer Applications in Power Systems
# Author: Laura Laringe
# Date: 2020-04-30
#
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import *
from Classes.Node import Node
from Classes.Substation import Substation
from Classes.BaseVoltage import BaseVoltage
from Classes.BusBar import BusBar
from Classes.LinearShuntCompensator import LinearShuntCompensator
from Classes.VoltageLevel import VoltageLevel
from Classes.PowerTransformer import PowerTransformer
from Classes.ACLine import ACLine
from Classes.Terminal import Terminal
from Classes.Breaker import Breaker
from Classes.GeneratingUnit import GeneratingUnit
from Classes.SynchronousMachine import SynchronousMachine
from Classes.RegulatingControl import RegulatingControl
from Classes.EnergyConsumer import EnergyConsumer
from Classes.PowerTransformerEnd import PowerTransformerEnd
from Classes.RatioTapChanger import RatioTapChanger
import pandapower.plotting.to_html as simple_plotly
import pandapower.topology as top
import tkinter as tk

#Import the ElementTree library
import xml.etree.ElementTree as ET

#import the pandapower module
import pandapower as pp

#create an empty network
#from ConnectionsFinder import find_attached_busbar
from TopologyGenerator import topology_generator




net = pp.create_empty_network()

#Creation of a tree by parsing the XML file referenced
# Select files in the GUI
def open_file():
    file = askopenfilename(filetypes =(("xml File", "*.xml"),("All Files","*.*")),
                           title = "Choose a file.")
    return file

answer = messagebox.showinfo(title="Assignment 1, Laura Laringe", message=("Insert EQ file"))
tree_EQ= ET.parse(open_file())
answer = messagebox.showinfo(title="Assignment 1, Laura Laringe", message=("Insert SSH file"))
tree_SSH = ET.parse(open_file())

#tree_EQ = ET.parse('MicroGridTestConfiguration_T1_BE_EQ_V2.xml')
#tree_SSH = ET.parse('MicroGridTestConfiguration_T1_BE_SSH_V2.xml')

#Access the root of the tree
microgrid = tree_EQ.getroot()
microgrid_SSH = tree_SSH.getroot()

#Creating a dictionary to store the namespace names and the URLs so that it is possible to
#reference the namespace to get the URL

ns = {'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

# fix the problem of dual use of the curly braces in python dictionaries and the XML namespace tags.
for equipment in microgrid.findall('.//*', ns):
    # clean the tags of all elements
    equipment.tag = equipment.tag.replace("{"+ns['cim']+"}","")
    equipment.tag = equipment.tag.replace("{" + ns['entsoe'] + "}", "")
    equipment.tag = equipment.tag.replace(ns['rdf'], "")


    # clean the attributes of all elements
    #print(equipment.attrib)
    if equipment.attrib:
        for mykey in equipment.attrib.keys():
            clean_key = mykey.replace(ns['rdf'], "")
            equipment.attrib[clean_key] = equipment.attrib.pop(mykey)

# fix the problem of dual use of the curly braces in python dictionaries and the XML namespace tags.
for equipment in microgrid_SSH.findall('.//*', ns):
    # clean the tags of all elements
    equipment.tag = equipment.tag.replace("{"+ns['cim']+"}","")
    equipment.tag = equipment.tag.replace("{" + ns['entsoe'] + "}", "")
    equipment.tag = equipment.tag.replace(ns['rdf'], "")


    # clean the attributes of all elements
    #print(equipment.attrib)
    if equipment.attrib:
        for mykey in equipment.attrib.keys():
            clean_key = mykey.replace(ns['rdf'], "")
            equipment.attrib[clean_key] = equipment.attrib.pop(mykey)


# initialize lists
base_voltage_list = []
busbar_list = []
linear_shunt_compensator_list = []
substation_list = []
voltage_level_list = []
generating_unit_list = []
synchronous_machine_list = []
regulating_control_list = []
power_transformer_list = []
energy_consumer_list = []
power_transformer_end_list = []
breaker_list = []
ratio_tap_changer_list = []
AC_lines_list = []


# Add elements into classes and corrispondend lists


# Create a dictonary to find the base voltage id
base_voltage_dict = {}
for ids in microgrid.findall('VoltageLevel'):
    vn = ids.find('VoltageLevel.BaseVoltage').attrib['resource']
    id = ids.get('ID')
    base_voltage_dict[id] = vn

# Create a dictionary to find nominal voltage value
nominal_voltage_dict = {}
for ids in microgrid.findall('VoltageLevel'):
    vn = float(ids.find('IdentifiedObject.name').text)
    id = ids.get('ID')
    nominal_voltage_dict[id] = vn

# Base Voltage
for volt in microgrid.findall('BaseVoltage'):
    ID= volt.get('ID')
    name= volt.find('BaseVoltage.nominalVoltage').text
    baseV = volt.find('BaseVoltage.nominalVoltage').text
    base_voltage_list.append(BaseVoltage(ID, name, baseV))

# Busbar Section
for bus in microgrid.findall('BusbarSection'):
    ID = bus.get('ID')
    name = bus.find('IdentifiedObject.name').text
    equipmentCont = bus.find('Equipment.EquipmentContainer').attrib['resource']
    voltage = nominal_voltage_dict[equipmentCont[1:]]
    busbar_list.append(BusBar(ID, name, equipmentCont, voltage))

#Linear Shunt Compensator
for compensator in microgrid.findall('LinearShuntCompensator'):
    ID = compensator.get('ID')
    name = compensator.find('IdentifiedObject.name').text
    b = float(compensator.find('LinearShuntCompensator.bPerSection').text)
    g = float(compensator.find('LinearShuntCompensator.gPerSection').text)
    equipmentCont = compensator.find('Equipment.EquipmentContainer').attrib['resource']
    voltage = float(compensator.find('ShuntCompensator.nomU').text)
    p = 0
    q = float(b * voltage**2)
    linear_shunt_compensator_list.append(LinearShuntCompensator(ID, name, b, g, equipmentCont, voltage, p, q))


# Substation
for sub in microgrid.findall('Substation'):
    ID = sub.get('ID')
    name = sub.find('IdentifiedObject.shortName').text
    region = sub.find('Substation.Region').attrib['resource']
    substation_list.append(Substation(ID, name, region))

# Voltage Level
for volt in microgrid.findall('VoltageLevel'):
    ID = volt.get('ID')
    name= volt.find('IdentifiedObject.name').text
    SS= volt.find('VoltageLevel.Substation').attrib['resource']
    Voltage= volt.find('VoltageLevel.BaseVoltage').attrib['resource']
    voltage_level_list.append(VoltageLevel(ID, name, SS, Voltage))

# Generating Unit
for unit in microgrid.findall('GeneratingUnit'):
    ID = unit.get('ID')
    name = unit.find('IdentifiedObject.name').text
    maxP = float(unit.find('GeneratingUnit.maxOperatingP').text)
    minP = float(unit.find('GeneratingUnit.minOperatingP').text)
    power = float(unit.find('GeneratingUnit.nominalP').text)
    equipment = unit.find('Equipment.EquipmentContainer').attrib['resource']
    generating_unit_list.append(GeneratingUnit(ID, name, maxP, minP,power, equipment))

# Function that returns P and Q from SSH file
P = []
Q = []

for gg in microgrid_SSH.findall('EnergyConsumer'):
    P.append(gg.find('EnergyConsumer.p').text)
    Q.append(gg.find('EnergyConsumer.q').text)
# Synchronous Machines
for i,machine in enumerate(microgrid.findall('SynchronousMachine')):
        ID = machine.get('ID')
        name = machine.find('IdentifiedObject.name').text
        rateS = float(machine.find('RotatingMachine.ratedS').text)
        gen_unit = machine.find('RotatingMachine.GeneratingUnit').attrib['resource']
        regContr = machine.find('RegulatingCondEq.RegulatingControl').attrib['resource']
        equipmentCont = machine.find('Equipment.EquipmentContainer').attrib['resource']
        baseVol=base_voltage_dict[equipmentCont[1:]]

        synchronous_machine_list.append(SynchronousMachine(ID, name, rateS, P[i], Q[i], gen_unit, regContr, equipmentCont, baseVol))




# RegulatingControl
targetValue = []

for control in microgrid_SSH.findall('RegulatingControl'):
    targetValue.append(control.find('RegulatingControl.targetValue').text)

for control in microgrid.findall('RegulatingControl'):
    ID = control.get('ID')
    name = control.find('IdentifiedObject.name').text

    regulating_control_list.append(RegulatingControl(ID, name, targetValue))

# Power Transformer
for transformer in microgrid.findall('PowerTransformer'):
    ID = transformer.get('ID')
    name = transformer.find('IdentifiedObject.name').text
    equipmentCont = transformer.find('Equipment.EquipmentContainer').attrib['resource']
    power_transformer_list.append(PowerTransformer(ID, name, equipmentCont))

# Energy Consumer
P = []
Q = []

for ec in microgrid_SSH.findall('EnergyConsumer'):
    P.append(float(ec.find('EnergyConsumer.p').text))
    Q.append(float(ec.find('EnergyConsumer.q').text))

for i,ec in enumerate(microgrid.findall('EnergyConsumer')):
    ID = ec.get('ID')
    name = ec.find('IdentifiedObject.name').text
    equipmentCont = ec.find('Equipment.EquipmentContainer').attrib['resource']
    baseVol = base_voltage_dict[equipmentCont[1:]]

    energy_consumer_list.append(EnergyConsumer(ID, name, P[i], Q[i], equipmentCont, baseVol))


# Power Transformers End
for pt in microgrid.findall('PowerTransformerEnd'):
    ID = pt.get('ID')
    name = pt.find('IdentifiedObject.name').text
    r = float(pt.find('PowerTransformerEnd.r').text)
    x = float(pt.find('PowerTransformerEnd.x').text)
    s = float(pt.find('PowerTransformerEnd.ratedS').text)
    IDTransformer = pt.find('PowerTransformerEnd.PowerTransformer').attrib['resource']
    baseVol = pt.find('TransformerEnd.BaseVoltage').attrib['resource']
    terminal = pt.find('TransformerEnd.Terminal').attrib['resource']
    powerTransformer = pt.find('PowerTransformerEnd.PowerTransformer').attrib['resource']
    end_number = pt.find('TransformerEnd.endNumber').text

    power_transformer_end_list.append(PowerTransformerEnd(ID, name, r, x, s, IDTransformer,
                                baseVol, terminal, powerTransformer, end_number))


# Breaker
for breaker in microgrid.findall('Breaker'):
    ID = breaker.get('ID')
    name = breaker.find('IdentifiedObject.name').text
    state = breaker.find('Switch.normalOpen').text
    equipmentCont = breaker.find('Equipment.EquipmentContainer').attrib['resource']
    baseVol = base_voltage_dict[equipmentCont[1:]]

    breaker_list.append(Breaker(ID, name, state, equipmentCont, baseVol))


 # Ratio Tap Changer
for rtc in microgrid.findall('RatioTapChanger'):
    ID = rtc.get('ID')
    name = rtc.find('IdentifiedObject.name').text
    step = rtc.find('TapChanger.normalStep').text

    ratio_tap_changer_list.append(RatioTapChanger(ID, name, step))

 # AC Line
for line in microgrid.findall('ACLineSegment'):
    ID = line. get('ID')
    name = line. find('IdentifiedObject.name').text
    equipmentCont = line. find('Equipment.EquipmentContainer').attrib['resource']
    lenght = float(line.find('Conductor.length').text)
    r = float(line. find('ACLineSegment.r').text)
    x = float(line. find('ACLineSegment.x').text)
    b = float(line. find('ACLineSegment.bch').text)
    g = float(line. find('ACLineSegment.gch').text)
    baseV = line. find('ConductingEquipment.BaseVoltage').attrib['resource']

    AC_lines_list.append(ACLine(ID, name, equipmentCont, lenght, r, x, b, g, baseV))

# Run the algorithm contained in the function
everything_stack, CE_stack = topology_generator(microgrid, microgrid_SSH, base_voltage_list, busbar_list, linear_shunt_compensator_list,
                       substation_list, voltage_level_list, generating_unit_list, regulating_control_list,
                       power_transformer_list, energy_consumer_list, power_transformer_end_list, breaker_list,
                       ratio_tap_changer_list, synchronous_machine_list, AC_lines_list)
print('stack representing all the nodes in order= ', everything_stack)
print('stack representing all the conducting equipment in order:', CE_stack)




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


# # In this part the data needed to make a pandapower network will be found
terminal_volt_dict = {}
for transformerend in power_transformer_end_list:
    tte = transformerend.terminal
    terminal_volt_dict[tte[1:]] = transformerend

base_volt_dict = {}
for voltage in base_voltage_list:
    baseVol = voltage.ID
    base_voltage = voltage.name
    base_volt_dict[baseVol] = base_voltage

# BUS
for bus in busbar_list:
    pp.create_bus(net, name=bus.name, vn_kv=bus.voltage, type="b")

# Transformer
for transformer in power_transformer_list:
    bus_list, way_terminals = find_attached_busbar(transformer)
    for bus, wt in zip(bus_list, way_terminals):
        if terminal_volt_dict[wt].end_number == '1':
            bus_high = bus
            hv_bus = pp.get_element_index(net, "bus", bus.name)
            vn =  terminal_volt_dict[wt].baseVol
            vn_hv_kv = base_volt_dict[vn[1:]]
            sn_mva = terminal_volt_dict[wt].s
        elif terminal_volt_dict[wt].end_number == '2':
            bus_low = bus
            lv_bus = pp.get_element_index(net, "bus", bus.name)
            vn = terminal_volt_dict[wt].baseVol
            vn_lv_kv = base_volt_dict[vn[1:]]

    pp.create_transformer_from_parameters(net, name=transformer.name, hv_bus =hv_bus, lv_bus =lv_bus, sn_mva = sn_mva, vn_hv_kv = vn_hv_kv,
                                          vn_lv_kv = vn_lv_kv, vkr_percent=10, vk_percent=0.3, pfe_kw=0, i0_percent=0)

# Shunt
for shunt in linear_shunt_compensator_list:
    bus, way_terminals = find_attached_busbar(shunt)
    bus_name = bus[0].name
    bus_pp = pp.get_element_index(net, "bus", bus_name)
    pp.create_shunt(net, name=shunt.name, bus= bus_pp, p_mw = shunt.p, q_mvar = shunt.q)

# Load
for load in energy_consumer_list:
    bus, way_terminals = find_attached_busbar(load)
    bus_name = bus[0].name
    bus_pp = pp.get_element_index(net, "bus", bus_name)
    pp.create_load(net, name=load.name, bus= bus_pp, p_mw=load.P)

# Line
for line in AC_lines_list:
    bus_list, way_terminals = find_attached_busbar(line)
    from_bus = pp.get_element_index(net, "bus", bus_list[0].name)
    to_bus = pp.get_element_index(net, "bus", bus_list[1].name)
    pp.create_line_from_parameters(net, name=line.name, from_bus= from_bus, to_bus=to_bus, length_km=line.lenght,
                                   r_ohm_per_km= line.r, x_ohm_per_km= line.x, c_nf_per_km=0, max_i_ka=0)

# Switch
for switch in breaker_list:
    bus, way_terminals = find_attached_busbar(switch)
    if switch.state == 'false':
        state = False
    else:
        state = True
    if isinstance(bus, list):
        from_bus = pp.get_element_index(net, "bus", bus[0].name)
        to_bus = pp.get_element_index(net, "bus", bus[1].name)
        pp.create_switch(net, from_bus, to_bus, et='b',
        type=state, name=switch.name)
    else:
        bus = pp.get_element_index(net, "bus", bus.name)
        list = find_CE_list(switch)
        for ce in list:
           if not check_busbar(ce):
                type = ce_type(ce)
                pp.create_switch(net, name=switch.name, bus=bus, et=type)

# Generator
for generator in generating_unit_list:
    bus, way_terminals = find_attached_busbar(generator)
    bus_name = bus[0].name
    bus_pp = pp.get_element_index(net, "bus", bus_name)
    pp.create_gen(net, name=generator.name, bus= bus_pp, p_mw= generator.power)


simple_plotly(net, 'network.html')

import tkinter as tk

OptionList = list([element.name for element in everything_stack])

app = tk.Tk()

app.geometry('700x400')

variable = tk.StringVar(app)
variable.set(OptionList[0])

answer = messagebox.showinfo(title="Assignment 1, Laura Laringe", message=("Now, you can choose to "
                                                                           "display any node's information"))

Label(app, text="Select a node to display its information!")
opt = tk.OptionMenu(app, variable, *OptionList)
opt.config(width=200, font=('Helvetica', 12))
opt.pack(side="top")


labelTest = tk.Label(text="", font=('Helvetica', 12), fg='red')
labelTest.pack(side="top")

def callback(*args):
    labelTest.configure(text="The selected item has these parameters:")
    labelTest.configure(text ="name: {}" .format(variable.get()))
    for node in everything_stack:
        if "{}".format(variable.get()) == node.name:
            attrs = vars(node)
            labelTest.configure(text =', '.join("%s: %s" % item for item in attrs.items()))


variable.trace("w", callback)

app.mainloop()

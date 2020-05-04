# Assignment 1  EH2745 Computer Applications in Power Systems
# Author: Laura Laringe
# Date: 2020-04-30
#
from tkinter.filedialog import askopenfilename

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

window = tk.Tk()
label = tk.Label(
    text="Assignment EH2745, Laura Laringe",
    foreground="white",  # Set the text color to white
    background="red"  # Set the background color to black
)
label.pack()
text_box = tk.Text()



net = pp.create_empty_network()

#Creation of a tree by parsing the XML file referenced
# Select files in the GUI
def open_file():
    file = askopenfilename(filetypes =(("xml File", "*.xml"),("All Files","*.*")),
                           title = "Choose a file.")
    return file


tree_EQ= ET.parse(open_file())
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
#
# # find_attached_busbar = connections_finder(microgrid, microgrid_SSH, base_voltage_list, busbar_list, linear_shunt_compensator_list,
# #                       substation_list, voltage_level_list, generating_unit_list, regulating_control_list,
# #                       power_transformer_list, energy_consumer_list, power_transformer_end_list, breaker_list,
# #                       ratio_tap_changer_list, synchronous_machine_list, AC_lines_list)
# #
#
# # In this part the data needed to make a pandapower network will be found
# terminal_volt_dict = {}
# for transformerend in power_transformer_end_list:
#     tte = transformerend.terminal
#     terminal_volt_dict[tte[1:]] = transformerend
#
# base_volt_dict = {}
# for voltage in base_voltage_list:
#     baseVol = voltage.ID
#     base_voltage = voltage.name
#     base_volt_dict[baseVol] = base_voltage
#
# # BUS
# for bus in busbar_list:
#     pp.create_bus(net, name=bus.name, vn_kv=bus.voltage, type="b")
#
# # Transformer
# for transformer in power_transformer_list:
#     bus_list, way_terminals = cf.find_attached_busbar(transformer)
#     for bus, wt in zip(bus_list, way_terminals):
#         if terminal_volt_dict[wt].end_number == '1':
#             bus_high = bus
#             hv_bus = pp.get_element_index(net, "bus", bus.name)
#             vn =  terminal_volt_dict[wt].baseVol
#             vn_hv_kv = base_volt_dict[vn[1:]]
#             sn_mva = terminal_volt_dict[wt].s
#         elif terminal_volt_dict[wt].end_number == '2':
#             bus_low = bus
#             lv_bus = pp.get_element_index(net, "bus", bus.name)
#             vn = terminal_volt_dict[wt].baseVol
#             vn_lv_kv = base_volt_dict[vn[1:]]
#
#     pp.create_transformer_from_parameters(net, name=transformer.name, hv_bus =hv_bus, lv_bus =lv_bus, sn_mva = sn_mva, vn_hv_kv = vn_hv_kv,
#                                           vn_lv_kv = vn_lv_kv, vkr_percent=10, vk_percent=0.3, pfe_kw=0, i0_percent=0)
#
#
# # Shunt
# for shunt in linear_shunt_compensator_list:
#     bus, way_terminals = cf.find_attached_busbar(shunt)
#     bus_name = bus[0].name
#     bus_pp = pp.get_element_index(net, "bus", bus_name)
#     pp.create_shunt(net, name=shunt.name, bus= bus_pp, p_mw = shunt.p, q_mvar = shunt.q)
#
# # Load
# for load in energy_consumer_list:
#     bus, way_terminals = cf.find_attached_busbar(load)
#     bus_name = bus[0].name
#     bus_pp = pp.get_element_index(net, "bus", bus_name)
#     pp.create_load(net, name=load.name, bus= bus_pp, p_mw=load.P)
#
# # Line
# for line in AC_lines_list:
#     bus_list, way_terminals = cf.find_attached_busbar(line)
#     from_bus = pp.get_element_index(net, "bus", bus_list[0].name)
#     to_bus = pp.get_element_index(net, "bus", bus_list[1].name)
#     pp.create_line_from_parameters(net, name=line.name, from_bus= from_bus, to_bus=to_bus, length_km=line.lenght,
#                                    r_ohm_per_km= line.r, x_ohm_per_km= line.x, c_nf_per_km=0, max_i_ka=0)
#
# # # Switch
# # for switch in breaker_list:
# #     bus, way_terminals = cf.find_attached_busbar(switch)
# #     if switch.state == 'false':
# #         state = False
# #        else:
# #          state = True
# #     if lenght(bus) == 2:
# #         from_bus = pp.get_element_index(net, "bus", bus[0].name)
# #         to_bus = pp.get_element_index(net, "bus", bus[1].name)
# #         pp.create_switch(net, from_bus, to_bus, et='b',
# #         type=state, name=switch.name)
# #     if lenght(bus) == 1:
# #         bus = pp.get_element_index(net, "bus", bus[0].name)
# #         list = find_CE_list(switch)
# #         for ce in list:
# #            if its not a bus:
# #                 type = find the type
# #
# #
# #     bus_name = bus[0].name
# #     bus_pp = pp.get_element_index(net, "bus", bus_name)
# #     #pp.create_switch(net, index=switch.ID, name=switch.name, bus=bus, element= 'b', et=b)
#
# # Generator
# for generator in generating_unit_list:
#     bus, way_terminals = cf.find_attached_busbar(generator)
#     bus_name = bus[0].name
#     bus_pp = pp.get_element_index(net, "bus", bus_name)
#     pp.create_gen(net, name=generator.name, bus= bus_pp, p_mw= generator.power)
#
# simple_plotly(net, 'network.html')
#
# mg=top.create_nxgraph(net, respect_switches = False)
#
#
#

window.mainloop()
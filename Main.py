# Assignment 1  EH2745 Computer Applications in Power Systems
# Author: Laura Laringe
# Date: 2020-04-20
#

from Classes.Node import Node
from Classes.Substation import Substation
from Classes.BaseVoltage import BaseVoltage
from Classes.BusBar import BusBar
from Classes.LinearShuntCompensator import LinearShuntCompensator
from Classes.VoltageLevel import VoltageLevel
from Classes.PowerTransformer import PowerTransformer
from Classes.ACLine import ACLine
from Classes.Terminal import Terminal
from Classes.Equipment import Equipment
from Classes.Breaker import Breaker
from Classes.GeneratingUnit import GeneratingUnit
from Classes.SynchronousMachine import SynchronousMachine
from Classes.RegulatingControl import RegulatingControl
from Classes.EnergyConsumer import EnergyConsumer
from Classes.PowerTransformerEnd import PowerTransformerEnd
from Classes.RatioTapChanger import RatioTapChanger


#Import the ElementTree library
import xml.etree.ElementTree as ET

#import the pandapower module
import pandapower as pp
import pandas as pd

#create an empty network
from TopologyGenerator import topology_generator

net = pp.create_empty_network()

#Creation of a tree by parsing the XML file referenced
#tree_EQ = ET.parse('Assignment_EQ_reduced.xml')
#tree_SSH = ET.parse('Assignment_SSH_reduced.xml')
tree_EQ = ET.parse('MicroGridTestConfiguration_T1_BE_EQ_V2.xml')
tree_SSH = ET.parse('MicroGridTestConfiguration_T1_BE_SSH_V2.xml')


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
    q = b * voltage**2
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

# Synchronous Machines
P = []
Q = []

for machine in microgrid_SSH.findall('SynchronousMachine'):
    P.append(float(machine.find('RotatingMachine.p').text))
    Q.append(float(machine.find('RotatingMachine.q').text))

for machine in microgrid.findall('SynchronousMachine'):
        ID = machine.get('ID')
        name = machine.find('IdentifiedObject.name').text
        rateS = float(machine.find('RotatingMachine.ratedS').text)
        gen_unit = machine.find('RotatingMachine.GeneratingUnit').attrib['resource']
        regContr = machine.find('RegulatingCondEq.RegulatingControl').attrib['resource']
        equipmentCont = machine.find('Equipment.EquipmentContainer').attrib['resource']
        baseVol=base_voltage_dict[equipmentCont[1:]]

        synchronous_machine_list.append(SynchronousMachine(ID, name, rateS, P, Q, gen_unit, regContr, equipmentCont, baseVol))


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

for ec in microgrid_SSH.findall(''):
    P.append(float(ec.find('EnergyConsumer.p').text))
    Q.append(float(ec.find('EnergyConsumer.q').text))

for ec in microgrid.findall('EnergyConsumer'):
    ID = ec.get('ID')
    name = ec.find('IdentifiedObject.name').text
    equipmentCont = ec.find('Equipment.EquipmentContainer').attrib['resource']
    baseVol = base_voltage_dict[equipmentCont[1:]]

    energy_consumer_list.append(EnergyConsumer(ID, name, P, Q, equipmentCont, baseVol))


# Power Transformers End
for pt in microgrid.findall('PowerTransformerEnd'):
    ID = pt.get('ID')
    name = pt.find('IdentifiedObject.name').text
    r = float(pt.find('PowerTransformerEnd.r').text)
    x = float(pt.find('PowerTransformerEnd.x').text)
    IDTransformer = pt.find('PowerTransformerEnd.PowerTransformer').attrib['resource']
    baseVol = pt.find('TransformerEnd.BaseVoltage').attrib['resource']
    terminal = pt.find('TransformerEnd.Terminal').attrib['resource']
    powerTransformer = pt.find('PowerTransformerEnd.PowerTransformer').attrib['resource']

    power_transformer_end_list.append(PowerTransformerEnd(ID, name, r, x, IDTransformer,
                                baseVol, terminal, powerTransformer))


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

# The result of the function will track all the connections between the elements contained in the XML file

# In this part the data needed to make a pandapower network will be found
print(CE_stack)
# Define function to check if element is a busbar
def check_busbar(curr_node):
    return isinstance(curr_node, BusBar)

def find_busbar(element):
    for bus in CE_stack:
        if check_busbar(bus):
            return bus
    return False

bus = find_busbar(CE_stack[1])
print(bus)

# BUS
for bus in busbar_list:
    pp.create_bus(net, index=bus.ID, name=bus.name, vn_kv=bus.voltage, type="b")

#print(net.bus)

# Shunt
#for shunt in linear_shunt_compensator_list:
#    pp.create_shunt(net, index=shunt.ID, name=shunt.name, p_mw= shunt.p, q_mvar= shunt.q)

# Load
for load in CE_stack:
    if isinstance(load, EnergyConsumer):
        if(not check_busbar(CE_stack.index(load)+1) and not check_busbar(CE_stack.index(load)-1)):
            print('no bus')
        else:
            print(check_busbar(CE_stack.index(load)+1), 'and' ,check_busbar(CE_stack.index(load)-1))
#for load in energy_consumer_list:
#     for ce in CE_stack:
#         if load==ce:
#             bus=
#     pp.create_load(net, index=load.ID, name=load.name, bus=bus)

# Line
for line in AC_lines_list:
    pass

# Switch
for switch in breaker_list:
    pass

# Generator
for generator in generating_unit_list:
    pass

# Transformer
for transformer in power_transformer_list:
    pass
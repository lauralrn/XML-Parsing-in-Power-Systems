# Assignment 1  EH2745 Computer Applications in Power Systems
# Author: Laura Laringe
# Date: 2020-04-20
#

from Classes.Node import Node
from Classes.Substation import Substation
from Classes.BaseVoltage import BaseVoltage
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
net = pp.create_empty_network()

#Creation of a tree by parsing the XML file referenced
#tree = ET.parse('MicroGridTestConfiguration_T1_BE_EQ_V2.xml')#
tree = ET.parse('Assignment_EQ_reduced.xml')
tree_S = ET.parse('Assignment_SSH_reduced.xml')

#Access the root of the tree
microgrid = tree.getroot()
microgrid_SSH = tree_S.getroot()

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
baseVoltageList = []
substationList = []
voltageLevelList = []
generatingUnitList = []
synchronousMachineList = []
regulatingControlList = []
powerTransformerList = []
energyConsumerList = []
powerTransformerEndList = []
breakerList = []
ratioTapChangerList = []
ACLinesList = []


# Add elements into classes and corrispondend lists


# Base Voltage
for volt in microgrid.findall('BaseVoltage'):
    IDBaseV = volt.get('ID')
    nameBaseV = volt.find('BaseVoltage.nominalVoltage').text
    baseV = volt.find('BaseVoltage.nominalVoltage').text
    baseVoltageList.append(BaseVoltage(IDBaseV, nameBaseV, baseV))

# Substation
for sub in microgrid.findall('Substation'):
    IDSS = sub.get('ID')
    nameSS = sub.find('IdentifiedObject.shortName').text
    regionSS = sub.find('Substation.Region').attrib['resource']
    substationList.append(Substation(IDSS, nameSS, regionSS))


# Voltage Level
for volt in microgrid.findall('VoltageLevel'):
    IDVLvl = volt.get('ID')
    nameVLvl = volt.find('IdentifiedObject.name').text
    SSVLvl = volt.find('VoltageLevel.Substation').attrib['resource']
    VoltageVLvl = volt.find('VoltageLevel.BaseVoltage').attrib['resource']
    voltageLevelList.append(VoltageLevel(IDVLvl, nameVLvl, SSVLvl, VoltageVLvl))






#create a dictonary to find vn_kn
voltage_dict = {}
for ids in microgrid.findall('cim:VoltageLevel', ns):
    vn = ids.find('cim:IdentifiedObject.name', ns).text
    id = ids.attrib.get(ns['rdf']+'ID')
    base_voltage_dict[id] = vn

#Create buses
for bus in microgrid.findall('cim:BusbarSection', ns):
    id= bus.attrib.get(ns['rdf']+'ID')
    name=bus.find('cim:IdentifiedObject.name', ns).text
    voltage=bus.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource')
    vn=base_voltage_dict[voltage[1:]]
    pp.create_bus(net, index=id, name=name, vn_kv=vn, type="b")

# for bus in microgrid.findall('cim:ConnectivityNode', ns):
#     id = bus.attrib.get(ns['rdf'] + 'ID')
#     name = bus.find('cim:IdentifiedObject.name', ns).text
#     voltage = bus.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource')
#     vn=base_voltage_dict[voltage[1:]]
#     pp.create_bus(net, index=id, name=name, vn_kv=vn, type="n")

#print(net.bus)

#Create lines


#dictiorary to find id to id of terminal
terminal_id_dict = {}
for terminals in microgrid.findall('cim:Terminal', ns):
    for equipments in terminals.findall('cim:Terminal.ConductingEquipment', ns):
        id = equipments.attrib.get(ns['rdf'] + 'resource')[1:]
        if id in terminal_id_dict:
            temp_list= list(terminal_id_dict[id])
            temp_list.append(terminals.attrib.get(ns['rdf'] + 'ID'))
            terminal_id_dict[id]=temp_list
        else:
            terminal_id=[]
            terminal_id.append(terminals.attrib.get(ns['rdf'] + 'ID'))
            terminal_id_dict[id]= terminal_id

#dictiorary to find bus name from terminal
bus_name_dict = {}
for terminals in microgrid.findall('cim:Terminal', ns):
    id = terminals.attrib.get(ns['rdf'] + 'ID')
    connectivity_node = terminals.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource')
    for nodes in microgrid.findall('cim:ConnectivityNode', ns):
        if (connectivity_node[1:]==nodes.attrib.get(ns['rdf'] + 'ID')):
            container = nodes.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource')
            for buses in microgrid.findall('cim:BusbarSection', ns):
                if(container == buses.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource')):
                    name = buses.find('cim:IdentifiedObject.name', ns).text
                    bus_name_dict[id]= name


#dictiorary to find bus from an ID  ## i cant do it i created the line without
line_to_bus_dict = {}
bus=[]
for element in microgrid:
    id = element.attrib.get(ns['rdf']+'ID')
    #print(id)
    #print(terminal_id_dict[id])
    #bus.append(bus_name_dict[terminal])
#line_to_bus_dict[id]=bus

#line creation
for line in microgrid.findall('cim:ACLineSegment', ns):
    id = line.attrib.get(ns['rdf'] + 'ID')
    lenght = line.find('cim:Conductor.length', ns).text
    r_ohm = line.find('cim:ACLineSegment.r', ns).text
    x_ohm = line.find('cim:ACLineSegment.x', ns).text
    c_nf = line.find('cim:ACLineSegment.bch', ns).text
    max_i= line.find('cim:ACLineSegment.shortCircuitEndTemperature', ns).text
    type = "NAYY 4x50 SE"
    terminal = []
    terminal = terminal_id_dict[id]
    print(terminal)
    name_from_bus= bus_name_dict[terminal[0]]
    print(name_from_bus)
    name_to_bus= bus_name_dict[terminal[1]]
    print(name_to_bus)
    line_from_bus = pp.get_element_index(net, "bus", name_from_bus)
    line_to_bus = pp.get_element_index(net, "bus", name_to_bus)
    pp.create_line_from_parameters(net, from_bus= line_from_bus, to_bus= line_to_bus, length_km=lenght, std_type=type, name=name, index=id, r_ohm_per_km=r_ohm, x_ohm_per_km=x_ohm, c_nf_per_km= c_nf, max_i_ka= max_i)

#print(net.line)
#Transformer

for transformer in microgrid.findall('cim:PowerTransformer', ns):
    id= transformer.attrib.get(ns['rdf']+'ID')
    name=transformer.find('cim:IdentifiedObject.name', ns).text
    hv=transformer.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource')
#    pp.create_transformer(net, index= id, hv_bus = 0, lv_bus = 1, name = name, std_type = "0.4 MVA 10/0.4 kV")

#hv_bus (int) - The bus on the high-voltage side on which the transformer will be connected to
#to find it, again i have to search for its id and find the terminal
#i would do a find bus library in which from an id i get to the buses. Howver i want high votlage and low voltage so i need two buses

#lv_bus (int) - The bus on the low-voltage side on which the transformer will be connected to

#for unit in microgrid.findall('cim:GeneratingUnit', ns):
 #   id= unit.attrib.get(ns['rdf']+'ID')
  #  name=unit.find('cim:IdentifiedObject.name', ns).text
   # hv=unit.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource')




#generating unit(id) --> synchronous machines(id) --> terminal(1) --> connectivity node --> container --> busbar
#generating unit --> synchronous machine --> equipment container --> busbar









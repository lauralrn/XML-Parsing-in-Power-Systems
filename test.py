
for line in microgrid.findall('cim:ACLineSegment', ns):
    bus = []
    id= line.attrib.get(ns['rdf'] + 'ID')
    lenght= line.find('cim:Conductor.length', ns).text
    r_ohm=  line.find('cim:ACLineSegment.r', ns).text
    x_ohm= line.find ('cim:ACLineSegment.x', ns).text
    type= "NAYY 4x50 SE"
    name=line.find('cim:IdentifiedObject.name', ns).text
    for ids in microgrid.findall('cim:Terminal', ns):
        terminal= ids.find('cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource')
        if (terminal[1:] == id):
            connectivity_node= ids.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource')
            for nodes in microgrid.findall('cim:ConnectivityNode', ns):
                connectivity_node_id=nodes.attrib.get(ns['rdf'] + 'ID')
                if (connectivity_node_id == connectivity_node):
                    container= ('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource')
                    for buses in microgrid('cim:BusbarSection', ns):
                        bus.append(buses.attrib.get(ns['rdf'] + 'ID'))
    pp.create_line(net, bus[0], bus[0], length_km=lenght, std_type=type, name=name, index=id, r_ohm_per_km=r_ohm, x_ohm_per_km=x_ohm)





for ids in microgrid.findall('cim:Terminal', ns):
    terminal= []
    terminal_connectivity_node = []
    terminal.append( ids.find('cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource'))
    for nodes in terminal:
        if (id==terminal[nodes])
            node= terminals.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource')[1:]
            terminal_connectivity_node.append(node)
    connectivity_node_id_dict[id] = terminal_connectivity_node



#Create dictiorary to find the ids of the buses connected to the line
connectivity_node_id_dict = {}
for ids in microgrid.findall('cim:Terminal', ns):
    terminal_connectivity_node = []
    id = []
    for terminals in ids.findall('cim:Terminal.ConductingEquipment', ns):
        id.append(terminals.attrib.get(ns['rdf'] + 'resource')[1:])
    if()
    node = terminals.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource')[1:]
    terminal_connectivity_node.append(node)
    connectivity_node_id_dict[id] = terminal_connectivity_nodez
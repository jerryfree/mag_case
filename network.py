import networkx as nx 
import os,sys,argparse,json
#import matplotlib.pylot as plt

def loadTopo(file):
    print("open ",file)
    G = nx.Graph()
    return G


def nxTest():
    G = nx.Graph()
    G.add_edge('A', 'B', weight=4)
    G.add_edge('B', 'D', weight=2)
    G.add_edge('A', 'C', weight=3)
    G.add_edge('C', 'D', weight=4)
    print(nx.shortest_path(G, 'A', 'D', weight='weight'))


def onPacket(pkt, ingestion):
  if macTable.get(pkt.l2.src, None) != ingestion:
    macTable.set(pkt.l2.src, ingestion, 500)
  dst = macTable.get(pkt.l2.dst, None)
  if dst == None:
    dsts = topo.hosts.values()
    path = stp(topo, ingestion, dsts)
    path = dirctionSt(spanningT, insgesion)
    return (ingestion, spanningedPorts[ingestion])
  else:
    path = shortestPath(topo, ingestion, dst)
  return path

def bind(ports,onPacket):#where does ingress/pkt come from ？
    if ingress in ports:
        onPacket(pkt,ingestion)



def format_latency(l):
        """ Helper method for parsing link latencies from the topology json. """
        if isinstance(l, str):
            return l
        else:
            return str(l) + "ms"

def parse_links(unparsed_links):
        """ Given a list of links descriptions of the form [node1, node2, latency, bandwidth]
            with the latency and bandwidth being optional, parses these descriptions
            into dictionaries and store them as self.links
        """
        links = []
        for link in unparsed_links:
            # make sure each link's endpoints are ordered alphabetically
            #print(link)
            s, t, = link[0], link[1]
            if s > t:
                s,t = t,s

            link_dict = {'node1':s,
                        'node2':t,
                        'latency':'0ms',
                        'bandwidth':None
                        }
            if len(link) > 2:
                link_dict['latency'] = format_latency(link[2])
            if len(link) > 3:
                link_dict['bandwidth'] = link[3]

            if link_dict['node1'][0] == 'h':
                assert link_dict['node2'][0] == 's', 'Hosts should be connected to switches, not ' + str(link_dict['node2'])
            links.append(link_dict)
        return links

def getsw(node):
    if node[0] == 'h':
        return node
    else :
        return node[0:2]

if __name__ == '__main__':
    #read topo construct graph
    topo_file = "./topology.json"
    with open(topo_file, 'r') as f:
        topo = json.load(f)
    hosts = topo['hosts']
    switchs = topo['switches']
    links = parse_links(topo['links'])
    
    #read binding conf
    binding_file = "./binding.json"
    with open(binding_file,'r') as f :
        binding = json.load(f)
    external_port = binding['external_port']
    all_port = binding['all_port']
    # print(external_port,all_port)

    #bind(external_port,onPacket)# ????

    G = nx.Graph()
    for link in links :      
        G.add_edge(link['node1'],link['node2'],weight = 1)
    for sw in switchs:
        for port in switchs[sw]:
            for port_temp in switchs[sw]:
                if port != port_temp and port_temp > port:
                    G.add_edge(port_temp,port,weight = 0.01)
    print("shortest path = ",nx.shortest_path(G,"h3","h2",weight = 'weight' ) )
    T = nx.minimum_spanning_tree(G,weight='weight')
    ST = sorted(T.edges)
    print("spainning tree = ",ST)
    GT = nx.Graph()
    GT.add_edges_from(ST)
    GTC = GT
    for node in nx.nodes(GT):
        numN = len(sorted(nx.neighbors(GT,node)))
        # print(numN)
        # print(node)
        # if numN == 1 and node[0] == 's':
        #     GTC.remove_node(node)
    # for node in nx.nodes(GT):
    #     numN = len(sorted(nx.neighbors(GT,node)))
    #     print(numN)
    #     print(node)
    # T = nx.minimum_spanning_tree(GT,weight='weight')
    # ST = sorted(T.edges)
    #switch level graph
#     GSW = nx.Graph()
#     GSW.add_nodes_from(hosts)
#     GSW.add_nodes_from(switchs)
#     for link in links :
#         sw1 = getsw(link['node1'])
#         sw2 = getsw(link['node2'])
#         GSW.add_edge(sw1,sw2,weight = 1)
#     T = nx.minimum_spanning_tree(GSW,weight='weight')
#     ST = sorted(T.edges)
#    # print(ST)
#    link_cnt = {}
#     for link in ST:
#         print(link)
#         if link[0] in link_cnt:
#             link_cnt[link[0]] + 1
#         else:

    
    

import networkx as nx 
import os,sys,argparse,json
from networkx.algorithms import approximation as ax

class maghelper:
    hosts =[]
    switchs = []
    links = {}
    external_port = []
    all_port =[]
    G ={}

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

    def topo_parser(self,topo_file):
        with open(topo_file, 'r') as f:
            topo = json.load(f)
        self.hosts = topo['hosts']
        self.switchs = topo['switches']
        self.links = maghelper.parse_links(topo['links'])

    def bingding_parser(self,bind_file):
        with open(bind_file,'r') as f :
            binding = json.load(f)
        self.external_port = binding['external_port']
        self.all_port = binding['all_port']
    
    def construct_graph(self):
        self.G = nx.Graph()
        for link in self.links :      
            self.G.add_edge(link['node1'],link['node2'],weight = 1)
        for sw in self.switchs:
            for port in self.switchs[sw]:
                for port_temp in self.switchs[sw]:
                    if port != port_temp and port_temp > port:
                        self.G.add_edge(port_temp,port,weight = 0.01)

    def shortest_path(self,src,dst):
        s_path = nx.shortest_path(self.G,src,dst,weight = 'weight' )
        g_path = []
        hop = 0
        while hop < (len(s_path)-1):
            if s_path[hop][0:2] == s_path[hop+1][0:2] :
                g_path.append( (s_path[hop],[s_path[hop+1]]) )
            hop = hop + 1 
     
        return g_path

    def steiner_tree(self ,src,dstes):
        steiner_t = ax.steinertree.steiner_tree(self.G,dstes)
        Dsteiner = steiner_t.to_directed()
        g_path =[]
        egress_port =[]
        cs_path =[] #muilt short path

        #get short path from src to each dst port
        for dst in dstes:
            short_p = nx.shortest_path(steiner_t,src,dst)
            
            if len(short_p) > 1 :
                print(short_p)
                hop = 0 
                g_short_path =[]
                while hop < (len(short_p)-1):
                    if short_p[hop][0:2] == short_p[hop+1][0:2] :
                        g_short_path.append( (short_p[hop],[short_p[hop+1]]) )
                    hop = hop + 1 
                cs_path.append(g_short_path)
            
        print("st short combine path =",cs_path)
        # in_swpipie={}
        # ingress_ports=[]#for path
        # egress_ports=[]#for swith
        # for path in cs_path :
        #     for insw_path in path:
        #         if ingress_ports.count(insw_path[0]) == 0 :
        #             ingress_ports.append(insw_path[0])
        # #print(ingress_ports)
        # for port in ingress_ports:
        #     for insw_path in cs_path:
        #         if insw_path[0] == port:
        #             egress_ports.append(insw_path[1])
                    # print(egress_ports)
                    
        #     g_path.append((port,egress_ports))
        #     egress_ports=[]
        # print("source_stener_path=",g_path)
        # for path in s_path:
        #     if len(path)>1:
        # for node in Dsteiner.nodes:
        #     for link in Dsteiner.edges:
        #         if link[0] == node and link[0][0:2] == link[1][0:2]:
        #             egress_port.append(link[1])
        #     g_path.append((node,egress_port))
        #     egress_port =[]
        # print("steiner_tree",g_path)


if __name__ == '__main__':
    #read topo construct graph
    topo_file = "./topology.json"
    magh = maghelper()
    magh.topo_parser(topo_file)
    #print(magh.links)
    
    #read binding conf
    binding_file = "./binding.json"
    magh.bingding_parser(binding_file)
    #print(magh.all_port)
    # print(external_port,all_port)

    #bind(external_port,onPacket)# ????

    magh.construct_graph()
    #print("shortest path = ",nx.shortest_path(magh.G,"h3","h2",weight = 'weight' ) )

    ST = ax.steinertree.steiner_tree(magh.G,magh.external_port)

    #T = nx.minimum_spanning_tree(G,weight='weight')
    SST = sorted(ST.edges)
    

    print("general s path =",magh.shortest_path('h1','h2'))

    magh.steiner_tree('s1-p1',magh.external_port)
    
import magellan as mg
from magellan.types import Map, Set, Port, Mac,sw
from external import shortestPath, steinerTree

macTable = Map(Mac, Port)()
swTable  = Map(Port,sw)
steiner_graph = steinerTree(topo,'external_port')

def mypath(graph,ingestion):
    globel_path = steinerPath(steiner_graph, ingestion)
    egress = globel_path.get_egressports(swTable.get(ingestion))
    path = shortestPath(steiner_graph,ingestion,egress)
    return path
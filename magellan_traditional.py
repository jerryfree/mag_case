import magellan as mg
from magellan.types import Map, Set, Port, Mac,sw
from external import shortestPath, steinerTree

macTable = Map(Mac, Port)()
swTable  = Map(Port,sw)
steiner_graph = steinerTree(topo,'external_port')

@mg.thread(label='all_port')
def onPacket(pkt, ingestion):
    if macTable.get(pkt.l2.src, None) is None:
        macTable[pkt.l2.src] = ingestion

    dst = macTable.get(pkt.l2.dst, None)
    if dst is None:
        globel_path = steinerPath(steiner_graph, ingestion)
        egress = globel_path.get_egressports(swTable.get(ingestion))
        path = shortestPath(steiner_graph,ingestion,egress)
    else:
        path = shortestPath( topo,ingestion, dst)
    return path
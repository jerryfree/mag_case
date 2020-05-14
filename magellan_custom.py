import magellan as mg
from magellan.types import Map, Set, Port, Mac
from external import shortestPath, steinerTree

macTable = Map(Mac, Port)()


@mthread(label='external_ports')
def onPacket(pkt, ingestion):
    if macTable.get(pkt.l2.src, None) is None:
        macTable[pkt.l2.src] = ingestion

    dst = macTable.get(pkt.l2.dst, None)
    if dst is None:
        path = steinerTree(topo, ingestion)
    else:
        path = shortestPath(topo, ingestion, dst)
    return path
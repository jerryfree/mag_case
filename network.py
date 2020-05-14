import networkx as nx 
import os,sys,argparse,json
from networkx.algorithms import approximation as ax


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


if __name__ == '__main__':

    bind(external_port,onPacket) 

    
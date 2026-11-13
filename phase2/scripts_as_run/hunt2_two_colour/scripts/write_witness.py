"""Write a circulant witness transcribed from a paper as (a) N:D text and (b) graph6 (edges = distances D).
Usage: python3 write_witness.py NAME N D1,D2,...   -> witnesses/NAME.circ and witnesses/NAME.g6"""
import sys, os, networkx as nx
name, n, D = sys.argv[1], int(sys.argv[2]), sorted({int(x) for x in sys.argv[3].split(',')})
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'witnesses')
open(os.path.join(out, name + '.circ'), 'w').write('%d:%s\n' % (n, ','.join(map(str, D))))
G = nx.circulant_graph(n, D)
open(os.path.join(out, name + '.g6'), 'wb').write(nx.to_graph6_bytes(G, header=False))
print(name, n, len(D), G.number_of_edges())

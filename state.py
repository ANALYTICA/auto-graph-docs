import neo4j
from langchain_community.graphs import Neo4jGraph
import os
import networkx as nx
import matplotlib.pyplot as plt
import math

#G = nx.Graph()
G = nx.DiGraph()

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"
graph = Neo4jGraph()

#graph.refresh_schema()
#print(graph.schema)


cypher = """
  MATCH (k:Keyword)-[:KEYWORD_OF]->(f:File)
  RETURN k, f
  """
print(graph.query(cypher), "\n\n\n")

cypher = """
  MATCH (f1:File)<-[:KEYWORD_OF]-(k:Keyword)-[:KEYWORD_OF]->(f2:File)
  RETURN k, f1, f2
  """
lst = graph.query(cypher)  
print(graph.query(cypher), "\n\n\n")

matches = []
for i in range(int(len(lst)/2)):
    print(lst[i]["f1"]["fileId"])
    matches.append([[lst[i]["f1"]["fileId"],lst[i]["f2"]["fileId"]], lst[i]["k"]["keywordId"]])

print(matches)

for con in matches:
    G.add_nodes_from([(con[0][0], {"type": "file"}), (con[0][1], {"type": "file"}), (con[1], {"type":"keyword"})])
    #G.add_edges_from([(con[0][0], con[1]), (con[0][1], con[1])])
    G.add_edges_from([(con[1], con[0][0]), (con[1], con[0][1])])

node_color = []
for node in G.nodes(data=True):
    print(node)
    if 'keyword' in node[1]['type']:
        node_color.append('#90EE90')
    else:
        node_color.append("#ADD8E6")

def draw_graph(nx_graph):
    fig, axes = plt.subplots(1,1,dpi=72)
    nx.draw(nx_graph, pos=nx.spring_layout(nx_graph,k=2/math.sqrt(nx_graph.order())), node_size=10000, node_color=node_color, width=5.0,arrowsize=50,font_size=20,  ax=axes, with_labels=True)
    #nx.draw(nx_graph, pos=nx.planar_layout(nx_graph), ax=axes, with_labels=True)
    #nx.draw(nx_graph, pos=nx.shell_layout(nx_graph), ax=axes, with_labels=True)
    #nx.draw(nx_graph, pos=nx.spiral_layout(nx_graph), ax=axes, with_labels=True)
    #nx.draw(nx_graph, pos=nx.circular_layout(nx_graph), ax=axes, with_labels=True)
    #nx.draw(nx_graph, pos=nx.kamada_kawai_layout(nx_graph), ax=axes, with_labels=True)
    plt.show()
    plt.savefig("myImagePDF.pdf", format="pdf", bbox_inches="tight")
draw_graph(G)

repeats = []
counts = []


for i in range(len(matches)):
    count = 1 
    words = []
    words.append(matches[i][1])
    if matches[i][0] in repeats:
        continue 
    for j in range(len(matches)):
        if j <= i:
            continue
        if matches[i][0] == matches[j][0]:
            count = count + 1
            words.append(matches[j][1])
    counts.append([matches[i][0], count, words])
    repeats.append(matches[i][0])


'''
for i in range(len(matches)):
    count = 1 
    if matches[i] in repeats:
        continue 
    for j in range(len(matches)):
        if j <= i:
            continue
        if matches[i] == matches[j]:
            count = count + 1
    counts.append([matches[i], count])
    repeats.append(matches[i])
'''

print(counts)


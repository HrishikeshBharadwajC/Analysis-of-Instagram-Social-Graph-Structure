import json
import networkx as nx
import matplotlib.pyplot as plt

data = {}
with open('location_data.txt') as file:
    data = json.load(file) 

graph = {}
edge_label = {}
G = nx.Graph()

loc_hash = {}

i=1
for locID1 in data:
    hashtags_all1 = set(data[locID1]['hashtags_all'])
    loc_hash[data[locID1]["location"]] = hashtags_all1
    for locID2 in data:
        if locID1 != locID2:
            hashtags_all2 = set(data[locID2]['hashtags_all'])
            inter = hashtags_all1.intersection(hashtags_all2)
            if inter:
                if (data[locID2]['location'],data[locID1]['location']) not in graph.keys():
                    print((data[locID1]['location'],data[locID2]['location']))
                    graph[(data[locID1]['location'],data[locID2]['location'])]=i
                    edge_label[i] = inter
                    i+=1
                    G.add_edge(data[locID1]['location'],data[locID2]['location'])       
                      
#community detect - CPM
from networkx.algorithms.community import k_clique_communities
coms = list(k_clique_communities(G, 4))
list(coms[0])
#----------------

print(edge_label)
pos = nx.spring_layout(G)
plt.figure()
nx.draw(G,pos,edge_color='black',width=1,linewidths=1,node_size=500,node_color='pink',alpha=0.9,labels={node:node for node in G.nodes()})
nx.draw_networkx_edge_labels(G,pos,edge_labels=graph,font_color='red')
plt.axis('off')
plt.show()

s_p = nx.spring_layout(G)
plt.axis("off")
nx.draw_networkx(G, pos = s_p, with_labels = False, node_size=35)
plt.show()


import community
s_p = nx.spring_layout(G)
parts = community.best_partition(G)
values = [parts.get(node) for node in G.nodes()]

comm_loc = {}
comm_hashtags = {}
for v in values:
    l = []
    comm_hashtags[v]=[]
    for p in parts:
        if parts[p] == v:
            l.append(p)
            comm_hashtags[v].extend(loc_hash[p])
    comm_loc[v]=l
    comm_hashtags[v] = [comm_hashtags[v], max(comm_hashtags[v],key=comm_hashtags[v].count)]
    
print("\n\n\n\n\n The communities Detected are: \n\n\n")
import pprint
pprint.PrettyPrinter(indent=4).pprint(comm_loc)

print("\n\n The community types are: \n")
print([ [k,comm_hashtags[k][1]] for k in comm_hashtags])


plt.axis("off")
nx.draw_networkx(G, pos = s_p, cmap = plt.get_cmap("jet"), node_color = values, node_size = 35, with_labels = False, width = 0)
plt.show()
#-------------
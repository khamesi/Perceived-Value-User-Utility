# -*- coding: utf-8 -*-
"""
GRAPH

@author: dolcev
"""
import networkx as nx
import networkx.algorithms.traversal as nt
import networkx.algorithms.connectivity as nc
from configuration import *
from collections import defaultdict

"""
create a graph with all nodes(devices) and edges(conditional prob)
from a conditional probability dicitonary
"""
def create_graph(cond_prob_dictionary, my_tipe):
    # create a directedgraph
    g = nx.DiGraph()
    
    # add nodes list
    g.add_nodes_from(folder_list)
    
    i = 0
    
    # add weight attribut to nodes
    for n in g.nodes() :
        #g.node[n]['weight'] = wattage_list[i]
        g.node[n]['Energy'] = energy_dic[n]
        g.node[n]['Utility'] = utility_dic[n]
        i = i +1
    
    # add edges 
    if my_tipe == 'functional':
        g = funct_binary_edges(g, cond_prob_dictionary)
    
    if my_tipe == 'preference':
        g = pref_binary_edges(g, cond_prob_dictionary)
    
    return g
    
"""
create a list with the conditional probabilitis as edges weight
"""
def add_edges_list(g, cond_prob_dictionary):
     
    for f in folder_list:
        # select the device
        temp = cond_prob_dictionary['condit_prob_'+ f]
        
        # for each other device except itself and when the weight is zero, select the conditional probability
        for k in folder_list:
            if (f == k or temp[k][1] ==0 ):
                continue
            else:   
                # add an edge for each couple of nodes with a not null weight
                g.add_edge(f, k, weight = temp[k][1])    # third parameter is the weight

    return g
    
    
"""
 catch the functional dependecies if the conditional prob is greater that 0.9
"""
def funct_binary_edges(g, cond_prob_dictionary):
     
    for f in folder_list:
        # select the device
        temp = cond_prob_dictionary['condit_prob_'+ f]
        
        # for each other device except itself and when the weight is zero, select the conditional probability
        for k in folder_list:
            if (f == k or temp[k][1] < 0.90 ):
                continue
            else:   
                # add an edge for each couple of nodes with a not null weight
                g.add_edge(f, k, weight = 1)    # third parameter is the weight

    return g
   
    
"""
 catch the preference dependecies if the conditional prob is between 0.2 and 0.9
"""
def pref_binary_edges(g, cond_prob_dictionary):
     
    for f in folder_list:
        # select the device
        temp = cond_prob_dictionary['condit_prob_'+ f]
        
        # for each other device except itself and when the weight is zero, select the conditional probability
        for k in folder_list:
            if (f == k or temp[k][1] < 0.20 or temp[k][1] >= 0.90):
                continue
            else:   
                # add an edge for each couple of nodes with a not null weight
                g.add_edge(f, k, weight = 1)    # third parameter is the weight

    return g    
    
"""
 get the weight of the direct edge between 2 nodes
"""
def get_weight(source, target, g):
    
    return g[source][target]['Energy']


"""   
 get th wattage of the current node
"""
def get_wattage(g, my_node):
    
    return g.node[my_node]['Energy']
    

"""
Breadth first search algorithm 
return a dictionary with all neighbors and a list of their sons for each one
"""
def bsf(g, source):
    
    return nt.bfs_successors(g, source)
    
"""
check if the neighbors of a node are included into the subset
and return the number of these 
""" 
def check_neighbors(current_dev, n):
    # n is list of neighbors
    
    # list of sub_set without the current device
    index = sub_set.index(current_dev)
    sublist = sub_set[:index] + sub_set[index+ 1 :]

    val = 0
    for i in n:
        if (i in sublist) == True:
            val = val + 1          
    
    return val
    
"""
Breadth First Depth Algorithm with depth limit
"""
def breadth_first_search(G, source, limit):
    d = defaultdict(list)
    
    # dictionary of the lenght between the source and all other nodes
    path_len = nx.shortest_path_length(G, source)
    
    for s,t in nt.bfs_edges(G,source):
        # if the corrent node depth is more than the limit, it'll not be in the final list
        if path_len[s] >= limit:
            continue
        else:
            d[s].append(t)
    
    # to create a list of all dependent devices of source until limit depth
    out = []
    for i in d.keys():
        out.extend(d[i]) 
    return out



"""
y_ij (preference graph)
Function to compute y_ij thus a vector for each device
that is 1 if the device i depends on device j
These values are sorted in alphabetic order
"""
def depend_vector(g):
    dic = {}
    l = sorted(g.nodes())
    
    for i in g.nodes():
        # create a zero vector whom lenght is the devices number
        vet = np.zeros(len(l))
        a = []

        for j in g.successors(i):
            a.append(l.index(j))
        
        vet[a] = 1
        dic[l.index(i)] = vet
    
    return dic

    
"""
y_ij (functional graph)
Function to compute y_ij thus a vector for each device
that is 1 if the device i depends on device j
In this function, the dependent devices are computed by the bsf algorithm
with a search depth equal to limit
"""
def bsf_depend_vector(g, limit):
    dic = {}
    l = sorted(g.nodes())
    
    for i in g.nodes():
        # create a zero vector whom lenght is the devices number
        vet = np.zeros(len(l))
        a = []

        for j in breadth_first_search(g, i, limit):
            a.append(l.index(j))
        
        vet[a] = 1
        dic[l.index(i)] = vet
    
    return dic

    
"""
Second version of Breadth First Depth Algorithm with depth limit
Gives the exact node number
"""
def bsf_depend_vector_2(g, limit):
    dic = {}
#     l = sorted(g.nodes())
    l = list(g.nodes())
    
    for i in g.nodes():
        # create a zero vector whom lenght is the devices number
        vet = np.zeros(len(l))
        a = []

        for j in breadth_first_search(g, i, limit):
            a.append(l.index(j))
        
        vet[a] = 1
#         dic[l.index(i)] = vet
        dic[i] = vet
    
    return dic
    
"""
Yij
dictionary with the number of all successors of each devices 
"""
def successors_number(dic_in):
    dic_out = {}
    
    for i in dic_in:
        dic_out[i] = sum(dic_in[i])
        
    return dic_out

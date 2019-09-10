import networkx as nx



def make_acyclic_scc(G):
    reduced = nx.condensation(G, scc=None)
    SCC_list= list(nx.strongly_connected_components(G))
    Super_nodes = {}
    
    for i in range(int(nx.number_strongly_connected_components(G))):
        Super_nodes[i] = list(SCC_list[i])
    
    return reduced, Super_nodes     

def make_acyclic(G):
    flag = 0
    G_REDUCED = G.copy()
    Cycles = nx.simple_cycles(G_REDUCED)
    Cycles_list = list(Cycles)
    if Cycles_list != []:
#         print('All cycles are: ' + str(Cycles_list))
        flag = 1
    else:
        print('No cycle found.')
        
    if flag == 1:
        while len(max(Cycles_list,key=len))>1:
            Cycles = nx.simple_cycles(G_REDUCED)
            Cycles_list = list(Cycles)
            bigest_Cycle = max(Cycles_list,key=len)
#             print('Bigest Cycle is: ' + str(bigest_Cycle) + ' with length of ' + str(len(bigest_Cycle)))

            for i in range(len(bigest_Cycle)-1):
                G_REDUCED = nx.contracted_nodes(G_REDUCED, bigest_Cycle[0], bigest_Cycle[i+1], self_loops=True)
#                 print('i = '+str(i))
                b2 = nx.simple_cycles(G_REDUCED)
                b2_list = list(b2)
#                 print('All cycles in g_reduced are: ' + str(b2_list))
                
        for i in range(len(b2_list)):
            G_REDUCED.remove_edge(b2_list[i][0],b2_list[i][0])

    return G_REDUCED





def make_acyclic_2(G):
    flag = 0
    G_REDUCED = G.copy()
    
    Super_nodes = {}
    for i in range(len(G_REDUCED.nodes())):
        Super_nodes[i] = [i]
        
    Cycles = nx.simple_cycles(G_REDUCED)
    Cycles_list = list(Cycles)
#     bigest_Cycle = max(Cycles_list,key=len)
    if Cycles_list != []:
#         print('All cycles are: ' + str(Cycles_list))
        flag = 1
    else:
        print('No cycle found.')
        
        
    if flag == 1:
        while len(max(Cycles_list,key=len))>1:
            Cycles = nx.simple_cycles(G_REDUCED)
            Cycles_list = list(Cycles)
            bigest_Cycle = max(Cycles_list,key=len)
        
#             print('Bigest Cycle is: ' + str(bigest_Cycle) + ' with length of ' + str(len(bigest_Cycle)))

            for i in range(len(bigest_Cycle)-1):
                G_REDUCED = nx.contracted_nodes(G_REDUCED, bigest_Cycle[0], bigest_Cycle[i+1], self_loops=True)
                Super_nodes[bigest_Cycle[0]].extend(Super_nodes[bigest_Cycle[i+1]])
                Super_nodes[bigest_Cycle[0]] = list(set(Super_nodes[bigest_Cycle[0]]))
                del Super_nodes[bigest_Cycle[i+1]]
#                 print('i = '+str(i))
                b2 = nx.simple_cycles(G_REDUCED)
                b2_list = list(b2)
#                 print('All cycles in g_reduced are: ' + str(b2_list))
                
        
        for i in range(len(b2_list)):
            G_REDUCED.remove_edge(b2_list[i][0],b2_list[i][0]) 

    return G_REDUCED, Super_nodes




def make_acyclic_3(funct_g_2):
    
    G_REDUCED_2 = funct_g_2.copy()
    Super_nodes = {}
    for i in range(len(G_REDUCED_2.nodes())):
        Super_nodes[i] = [i]

    A_Cycle = []
    try:
        A_Cycle = nx.find_cycle(G_REDUCED_2, orientation='original')
#         print(A_Cycle)
    except:
        pass

    while A_Cycle !=[]:
        for i in range(len(A_Cycle)-1):
#             print('i: '+str(i))
    #         print(A_Cycle)
            if (A_Cycle[0][0], A_Cycle[i+1][0]) in G_REDUCED_2.edges():
                G_REDUCED_2 = nx.contracted_nodes(G_REDUCED_2, A_Cycle[0][0], A_Cycle[i+1][0], self_loops=False)
                Super_nodes[A_Cycle[0][0]].extend(Super_nodes[A_Cycle[i+1][0]])
                Super_nodes[A_Cycle[0][0]] = list(set(Super_nodes[A_Cycle[0][0]]))
                del Super_nodes[A_Cycle[i+1][0]]
            else:
    #             break
                A_Cycle = []
    #     A_Cycle = nx.find_cycle(G_REDUCED_2, orientation='original')
        try:
            A_Cycle = nx.find_cycle(G_REDUCED_2, orientation='original')
#             print(A_Cycle)
        except:
            A_Cycle = []
            pass
        
    return G_REDUCED_2, Super_nodes



def Inverse_graph(G):
    G_inverse = nx.DiGraph(G)
#     G_inverse.add_node(G)
    for i in G.edges():
        G_inverse.remove_edge(i[0],i[1])
        G_inverse.add_edge(i[1],i[0])
        
    return G_inverse


def Super_Costs(Super_nodes,rand_cost):
    Cost_of_Super_nodes = {}
    for i in Super_nodes.keys():
        Cost_of_Super_nodes[i] = sum(rand_cost[i] for i in Super_nodes[i])
        
    return Cost_of_Super_nodes

def Super_Utilities(Super_nodes,rand_utility):
    Utility_of_Super_nodes = {}
    for i in Super_nodes.keys():
        Utility_of_Super_nodes[i] = sum(rand_utility[i] for i in Super_nodes[i])
        
    return Utility_of_Super_nodes
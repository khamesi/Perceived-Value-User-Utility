# -*- coding: utf-8 -*-
"""
This file contains fuctions to generate random graphs using the 
Erdos Renyi algorithm

@author: dolcev
"""
from configuration import *
import networkx as nx
import numpy as np
import random
import math
from milp import complete_milp
from sim_annealing import simulated_annealing, modified_simulated_annealing
from graph import depend_vector, bsf_depend_vector, successors_number
from knapsack_gurobi import knapsack, knapsack_2
from sim_annealing import cost_function
from Greedy_functions import *
# this is the seed to get the same graphs in different tests
random.seed(a = 1)

def directed_barabasi_albert_graph(n, m):

    G=nx.DiGraph()

    # Target nodes for new edges
    targets=list(range(m))
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes=[]
    # Start adding the other n-m nodes. The first node is m.
    source=m
    while source<n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source]*m,targets))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source]*m)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachement)
        targets = random.choices(repeated_nodes, weights=None, cum_weights=None, k=m)
        source += 1
        
    Permutation_dict={}
    index = 0
    for i in np.random.permutation(n):
        Permutation_dict[i]=index
        index+=1
    G_2 = nx.relabel_nodes(G, Permutation_dict, copy=True)
    return G_2

def directed_barabasi_albert_graph_2(n, m):

    G=nx.DiGraph()

    # Target nodes for new edges
#     targets=list(range(m))
    targets=list(range(math.ceil(n/2)))
    G.add_nodes_from(targets)
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes=[]
    # Start adding the other n-m nodes. The first node is m.
    source=math.ceil(n/2)
    while source<n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source]*m,targets))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source]*m)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachement)
        targets = random.choices(repeated_nodes, weights=None, cum_weights=None, k=m)
        source += 1
    Permutation_dict={}
    index = 0
    for i in np.random.permutation(n):
        Permutation_dict[i]=index
        index+=1
    G_2 = nx.relabel_nodes(G, Permutation_dict, copy=True)
    return G_2


"""
this generates a graph with n nodes and edge with probability p
"""
def new_random_graph(n, p):    
#     g = nx.erdos_renyi_graph(n, p, seed=None, directed=True)
    g = nx.DiGraph()
#     m = math.ceil(p*10)
    m = p
    if m>math.ceil(n/2):
        print('m can not be greater than '+str(math.ceil(n/2)))
        m = math.ceil(n/2)
    if m>0:
#         g = directed_barabasi_albert_graph(n, m)
        g = directed_barabasi_albert_graph_2(n, m)
    else:
        g.add_nodes_from(range(n))
    
    return g


"""
creating a sequence of m from 0 to 10 
"""
def range_m(n):
    
          
#     return np.arange(0, 1, 0.1)
#     return np.arange(0, n, 3)
    return np.arange(0, math.floor(n/2), 2)


"""
creating a sequence of probablity from 0 to 1 with 0.1 of step
"""
def range_probability():
          
#     return np.arange(0, 1, 0.1)
    return np.arange(0, 1, 0.1)


"""
creating a sequence of increasing numerbs of nodes from 10 to 1000 with 100 of step
"""   
def range_nodes():
          
#     return list(np.arange(10, 41, 5))
#     return range(10, 31, 5)
    return range(5, 41, 5)

    
"""
creating a sequence of increasing budget values from 500 to 10000 with 100 of step
"""    
def range_budget():
    
    return np.arange(10000, 55001, 5000)
    
    
"""
generating an array of random values between lb and ub
of wattage energy 
"""
def random_energy(n):    
    # lower and upper bound to generate random wattage value
    lb = 20
    up = 3000
    out = []    # output list

    for i in range(n):
        out.append(random.randint(lb, up))
        
    return out

    
"""
creating an array of random values between lb and ub
of devices utility
"""
def random_utility(n):    
    # lower and upper bound to generate random wattage value
    lb = 10
    up = 100
    out = []    # output list

    for i in range(n):
        out.append(random.randint(lb, up))
        
    return np.array(out)
    

"""
this funciton creates another graph from the the g1 graph 
and deleting some edges and adding them to the graph g2 
"""
def two_graphs(g1):
    # nodes list
    n = g1.nodes()
    
    g2 = nx.DiGraph()
    g2.add_nodes_from(n)
    
#     # select edges for the preferance graph with a probability 0.7
#     for e in list(g1.edges()):
#         flag = random.random() < 0.7
#         if flag == True:
#             g2.add_edge(e[0], e[1])
#             g1.remove_edge(e[0], e[1])
    
    # g1 is functional graph, g2 is preferance graph
    return g1, g2


    
""" MILP AND SIMULATED ANNEALING RANDOM PROBABILITY """
def random_probability_graphs(n, b):
    print('probability')
    # y and y lists to plot these values
    x_list = []    
    max_utilities = []

    y_list_MILP = []   
    y_list_SIM = []
    y_list_MODSIM = []
    y_list_KNAPSACK = []
    y_list_GREEDY = []
    y_list_ACYCLIC_GREEDY = []

    iterations_list_SIM = []      
#     iterations_list_MODSIM = []  
    iterations_list_MODSIM = iterations_list_SIM

    # random costs and utilities which remain constant for all probability values
    # random wattage energy list
    rand_cost = random_energy(n)        
    # random utility array
    rand_utility = random_utility(n)        
    # maximum utility of the current graph 
    current_max_utility = sum(rand_utility)    

#     for p in range_probability():
    for p in range_m(n):
        # it creates one random graph
        g = new_random_graph(n, p)
        
        # this function create another graph (functional graph) from the graph g
        funct_g, pref_g = two_graphs(g)     
                
        # compute the dependencies arrays 
        y_p = depend_vector(pref_g)       
        y_f = bsf_depend_vector(funct_g, n)    
        Y_p = successors_number(y_p)
        Y_f = successors_number(y_f) 
        
        # list of maximum utilities (IT'S THE SAME FOR ALL PORBABILITY VALUES)
        max_utilities.append(current_max_utility)
        # list of probability values (AXIS X)
        x_list.append(p)
        
        """  ********  MILP  ********  """
#         print('milp')
        m_milp, milp_sol = complete_milp(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)            
        # to get the objective function value (AXIS Y)
        obj = m_milp.getObjective()
        y_list_MILP.append(obj.getValue())        
                   
        """  ******* REGULAR SIMULATED ANNEALING  ********  """
#         print('regular sim ann')
        sol = (np.zeros(n))   
#        sol = list(np.zeros(n))   
#        cost = 0
#        while(cost > b):
#            sol = list(np.random.randint(2, size = n))
#            cost = cost_function(sol, rand_cost)
        #sol = list(np.random.randint(2, size = n))
        solution, u_val, iterations = simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_SIM.append(u_val)
        iterations_list_SIM.append(iterations)     
       
#         """  ******** MODIFIED SIMULATED ANNEALING ********* """
#         print('modified sim ann')

#         sol = list(np.zeros(n))     
#         solution, u_val, iterations = modified_simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
#         y_list_MODSIM.append(u_val)
#         iterations_list_MODSIM.append(iterations)
        
        """  ******* KNAPSACK  ********  """
#         print('knapsack')
        knapsack_utility, m, knap_sol = knapsack(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)
        y_list_KNAPSACK.append(knapsack_utility)
        
        """  ******* GREEDY  ********  """
#         print('greedy')
        greedy_solution, greedy_utility, greedy_cost, sorted_select_set = greedy_alg(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_GREEDY.append(greedy_utility)
        
        
        """  ******* ACYCLIC GREEDY  ********  """
#         print('acyclic greedy')
        Acyclic_solution, Acyclic_utility, Acyclic_cost= acyclic_greedy_alg(funct_g, y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_ACYCLIC_GREEDY.append(Acyclic_utility)
        
    # convert lists into arrays to compute division
    max_utilities_array = np.array(max_utilities)
    y_array_MILP = np.array(y_list_MILP)
    y_array_SIM = np.array(y_list_SIM)
    y_array_MODSIM = np.array(y_list_MODSIM)
    y_array_KNAPSACK = np.array(y_list_KNAPSACK)
    y_array_GREEDY = np.array(y_list_GREEDY)
    y_array_ACYCLIC_GREEDY = np.array(y_list_ACYCLIC_GREEDY)
    
    # compute the percentage utility
    final_y_MILP = 100 * (y_array_MILP / max_utilities_array)
    final_y_SIM = 100 * (y_array_SIM / max_utilities_array)
#     final_y_MODSIM = 100 * (y_array_MODSIM / max_utilities_array)
    final_y_MODSIM = final_y_SIM
    final_y_KNAPSACK = 100 * (y_array_KNAPSACK / max_utilities_array)
    final_y_GREEDY = 100 * (y_array_GREEDY / max_utilities_array)
    final_y_ACYCLIC_GREEDY = 100 * (y_array_ACYCLIC_GREEDY / max_utilities_array)
    
    
    # convert array into list
    final_y_MILP = list(final_y_MILP)
    final_y_SIM = list(final_y_SIM)
    final_y_MODSIM = list(final_y_MODSIM)
    final_y_KNAPSACK = list(final_y_KNAPSACK)
    final_y_GREEDY = list(final_y_GREEDY)
    final_y_ACYCLIC_GREEDY = list(final_y_ACYCLIC_GREEDY)
    
    return x_list, final_y_MILP, final_y_SIM, final_y_MODSIM, final_y_KNAPSACK, final_y_GREEDY, final_y_ACYCLIC_GREEDY, iterations_list_SIM, iterations_list_MODSIM
    
    
""" MILP AND SIMULATED ANNEALING RANDOM NODES """
        
def random_nodes_graphs(p, b):
    print('nodes')
    # y and y lists to plot these values
    max_utilities = []
    x_list = []    
    y_list_MILP = []
    y_list_SIM = []
    y_list_MODSIM = []
    y_list_KNAPSACK = []
    y_list_GREEDY = []
    y_list_ACYCLIC_GREEDY = []

    iterations_list_SIM = []  
#     iterations_list_MODSIM = []  
    iterations_list_MODSIM = iterations_list_SIM

    for n in range_nodes():
        print(n)
        # to create a new directed random graph
        g = new_random_graph(n, p)
        
        # this function create another graph (functional graph) from the graph g
        funct_g, pref_g = two_graphs(g)   
        
        # compute the dependencies arrays 
        y_p = depend_vector(pref_g)       
        y_f = bsf_depend_vector(funct_g, n)    
        Y_p = successors_number(y_p)
        Y_f = successors_number(y_f)
        
        # random wattage energy list
        rand_cost = random_energy(n)
        # random utility array
        rand_utility = random_utility(n)
        # maximum utility of the current graph 
        current_max_utility = sum(rand_utility)
        # list of maximum utilities
        max_utilities.append(current_max_utility)
        
        # list of probability values (AXIS X)
        x_list.append(n)
        
        """  ********  MILP  ********  """
#         print('milp')
        # to call the milp algortihm
        m_milp, milp_sol = complete_milp(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)        
        # to get the objective function value (AXIS Y)
        obj = m_milp.getObjective()
        y_list_MILP.append(obj.getValue())
        
        """  ********  SIMULATED ANNEALING  ********  """
#         print('regular sim ann')
        sol = (np.zeros(n))    
#        sol = list(np.zeros(n))  
#        cost = 0
#        while(cost > b):
#            sol = list(np.random.randint(2, size = n))
#            cost = cost_function(sol, rand_cost)
        #sol = list(np.random.randint(2, size = n))
        #solution, u_val, iterations = simulated_annealing2(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        solution, u_val, iterations = simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_SIM.append(u_val)
        iterations_list_SIM.append(iterations)
                 
#         """  ********  MODIFIED SIMULATED ANNEALING  ********  """
#         print('modified sim ann')
#         sol = list(np.zeros(n))        
#         solution, u_val, iterations = modified_simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
#         y_list_MODSIM.append(u_val)
#         iterations_list_MODSIM.append(iterations)                
                
        """  ******* KNAPSACK  ********  """
#         print('knapsack')
        knapsack_utility, m, knap_sol = knapsack(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)
        y_list_KNAPSACK.append(knapsack_utility)  
        
       
        """  ******* GREEDY  ********  """
#         print('greedy')
        greedy_solution, greedy_utility, greedy_cost, sorted_select_set = greedy_alg(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_GREEDY.append(greedy_utility)

#         # increase the nodes number
#         n = n + 5
 
        
        """  ******* ACYCLIC GREEDY  ********  """
#         print('acyclic greedy')
        Acyclic_solution, Acyclic_utility, Acyclic_cost= acyclic_greedy_alg(funct_g, y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_ACYCLIC_GREEDY.append(Acyclic_utility)
        
    # convert lists into arrays to compute division
    y_array_MILP = np.array(y_list_MILP)
    y_array_SIM = np.array(y_list_SIM)
    y_array_MODSIM = np.array(y_list_MODSIM)
    y_array_KNAPSACK = np.array(y_list_KNAPSACK)
    y_array_GREEDY = np.array(y_list_GREEDY)
    y_array_ACYCLIC_GREEDY = np.array(y_list_ACYCLIC_GREEDY)

    max_utilities_array = np.array(max_utilities)
    
    # compute the percentage utility
    final_y_MILP = 100 * (y_array_MILP / max_utilities_array)
    final_y_SIM = 100 * (y_array_SIM / max_utilities_array)
#     final_y_MODSIM = 100 * (y_array_MODSIM / max_utilities_array)
    final_y_MODSIM = final_y_SIM
    final_y_KNAPSACK = 100 * (y_array_KNAPSACK / max_utilities_array)
    final_y_GREEDY = 100 * (y_array_GREEDY / max_utilities_array)
    final_y_ACYCLIC_GREEDY = 100 * (y_array_ACYCLIC_GREEDY / max_utilities_array)
    
    # convert array into list
    final_y_MILP = list(final_y_MILP)
    final_y_SIM = list(final_y_SIM)
    final_y_MODSIM = list(final_y_MODSIM)
    final_y_KNAPSACK = list(final_y_KNAPSACK)
    final_y_GREEDY = list(final_y_GREEDY)
    final_y_ACYCLIC_GREEDY = list(final_y_ACYCLIC_GREEDY)
    
    return x_list, final_y_MILP, final_y_SIM, final_y_MODSIM, final_y_KNAPSACK, final_y_GREEDY, final_y_ACYCLIC_GREEDY, iterations_list_SIM, iterations_list_MODSIM


""" MILP AND SIMULATED ANNEALING RANDOM BUDGET """
def random_budget_graphs(n, p):
    print('budget')
    max_utilities = []  
    x_list = []
    y_list_MILP = []
    y_list_SIM = []
    y_list_MODSIM = []
    y_list_KNAPSACK = []
    y_list_GREEDY = []
    y_list_ACYCLIC_GREEDY = []
    
    iterations_list_SIM = []  
#     iterations_list_MODSIM = []  
    iterations_list_MODSIM = iterations_list_SIM

    # random wattage energy list
    rand_cost = random_energy(n)
    # random utility array
    rand_utility = random_utility(n)
    # maximum utility of the current graph 
    current_max_utility = sum(rand_utility)

    for b in range_budget():
        # it creates one random graph
        g = new_random_graph(n, p)
        
        # this function create another graph (functional graph) from the graph g
        funct_g, pref_g = two_graphs(g)     

        # compute the dependencies arrays 
        y_p = depend_vector(pref_g)       
        y_f = bsf_depend_vector(funct_g, n)    
        Y_p = successors_number(y_p)
        Y_f = successors_number(y_f)
        
        # list of maximum utilities
        max_utilities.append(current_max_utility)
        
        # list of probability values (AXIS X)
        x_list.append(b)
        
        """  ********  MILP  ********  """
#         print('milp')
        # to call the milp algortihm
        m_milp, milp_sol = complete_milp(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)
        # to get the objective function value (AXIS Y)
        obj = m_milp.getObjective()
        y_list_MILP.append(obj.getValue())
            
        
        """  ********  SIMULATED ANNEALING  ********  """
        print('regular sim ann')
        sol = np.zeros(n) # it starts with an empty subset  

#        sol = list(np.zeros(n))  
#        cost = 0
#        while(cost > b):
#            sol = list(np.random.randint(2, size = n))
#            cost = cost_function(sol, rand_cost)
            
        solution, u_val, iterations = simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_SIM.append(u_val)
        iterations_list_SIM.append(iterations)
           
        
#         """  ********  MODIFIED SIMULATED ANNEALING  ********  """
#         print('modified sim ann')
#         sol = list(np.zeros(n)) # it starts with an empty subset  
#         solution, u_val, iterations = modified_simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
#         y_list_MODSIM.append(u_val)
#         iterations_list_MODSIM.append(iterations)
                
        """  ******* KNAPSACK  ********  """
#         print('knapsack')
        knapsack_utility, m, knap_sol= knapsack(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)
        y_list_KNAPSACK.append(knapsack_utility)
        
        
               
        """  ******* GREEDY  ********  """
#         print('greedy')
        greedy_solution, greedy_utility, greedy_cost, sorted_select_set = greedy_alg(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_GREEDY.append(greedy_utility)
 
        
        """  ******* ACYCLIC GREEDY  ********  """
#         print('acyclic greedy')
        Acyclic_solution, Acyclic_utility, Acyclic_cost= acyclic_greedy_alg(funct_g, y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
        y_list_ACYCLIC_GREEDY.append(Acyclic_utility)

        
    # convert lists into arrays to compute division
    y_array_MILP = np.array(y_list_MILP)
    y_array_SIM = np.array(y_list_SIM)
    y_array_MODSIM = np.array(y_list_MODSIM)
    y_array_KNAPSACK = np.array(y_list_KNAPSACK)
    y_array_GREEDY = np.array(y_list_GREEDY)
    y_array_ACYCLIC_GREEDY = np.array(y_list_ACYCLIC_GREEDY)
    max_utilities_array = np.array(max_utilities)
    
    # compute the percentage utility
    final_y_MILP = 100 * (y_array_MILP / max_utilities_array)
    final_y_SIM = 100 * (y_array_SIM / max_utilities_array)
#     final_y_MODSIM = 100 * (y_array_MODSIM / max_utilities_array)
    final_y_MODSIM = final_y_SIM
    final_y_KNAPSACK = 100 * (y_array_KNAPSACK / max_utilities_array)
    final_y_GREEDY = 100 * (y_array_GREEDY / max_utilities_array)
    final_y_ACYCLIC_GREEDY = 100 * (y_array_ACYCLIC_GREEDY / max_utilities_array)
    
    # convert array into list
    final_y_MILP = list(final_y_MILP)        
    final_y_SIM = list(final_y_SIM)
    final_y_MODSIM = list(final_y_MODSIM)
    final_y_KNAPSACK = list(final_y_KNAPSACK)
    final_y_GREEDY = list(final_y_GREEDY)
    final_y_ACYCLIC_GREEDY = list(final_y_ACYCLIC_GREEDY)
    
    return x_list, final_y_MILP, final_y_SIM, final_y_MODSIM, final_y_KNAPSACK, final_y_GREEDY, final_y_ACYCLIC_GREEDY, iterations_list_SIM, iterations_list_MODSIM
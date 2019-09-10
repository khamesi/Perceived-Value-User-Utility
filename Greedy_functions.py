import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.optimize
import copy
import math
import networkx as nx
from main_functions import *    
from graph import create_graph, depend_vector, successors_number, bsf_depend_vector,depend_vector, bsf_depend_vector, successors_number
from milp import *
from random_graphs import * 
from sim_annealing import *
from configuration  import *
from save_plot import *
from Make_Acyclic import *

"""
Greedy Algorithm
"""


def greedy_alg(y_p, y_f, Y_p, Y_f, solution, cost_vector, u, B):
    
    n=len(solution)
    current_solution = copy.copy(solution)
    search_set = np.arange(n)
#     remained_set = remained_set - current_solution
    
    # compute the utility value of the current solution
    current_utility = compute_utility(y_p, y_f, Y_p, Y_f, current_solution, u)
    current_cost=cost_function(current_solution, cost_vector)
    
    for i in range(len(solution)):
        select_set=list()
        A=list()
        for k in search_set:
            temp_solution = copy.copy(current_solution)
            temp_solution[k]=1
            l = compute_utility(y_p, y_f, Y_p, Y_f, temp_solution, u)/ cost_vector[k]
            select_set.append((l, k))

        A=sorted(select_set, reverse=True)
        j = A[0][1]
#         print('j='+str(j))
        new_solution = copy.copy(current_solution)
        new_solution[j] = 1 
        new_utility = compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u)
        new_cost = cost_function(new_solution, cost_vector)
        b = np.array([j])
        search_set = np.setdiff1d(search_set,b)
#         print(search_set)
#         search_set = np.delete(search_set,j)
#         print(current_solution)
        
        if new_cost <= B:
            current_solution = copy.copy(new_solution)
#             print([int(i) for i in current_solution])
            current_utility = new_utility
            current_cost = new_cost
            
            
    print('Greedy Approach \n'+ 'Utility: ' + str(current_utility))# + '\n' + 'Cost: ' + str(current_cost))
    
    return current_solution, current_utility, current_cost, select_set

def greedy_alg_knapsack(y_p, y_f, Y_p, Y_f, solution, cost_vector, u,u_knap, B):
    
    n=len(solution)
    current_solution = copy.copy(solution)
    search_set = np.arange(n)
#     remained_set = remained_set - current_solution
    
    # compute the utility value of the current solution
    current_utility = compute_utility(y_p, y_f, Y_p, Y_f, current_solution, u)
    current_cost=cost_function(current_solution, cost_vector)
    
    for i in range(len(solution)):
        select_set=list()
        A=list()
        for k in search_set:
            temp_solution = copy.copy(current_solution)
            temp_solution[k]=1
            l = u_knap[k]
            select_set.append((l, k))

        A=sorted(select_set, reverse=True)
        j = A[0][1]
#         print('j='+str(j))
        new_solution = copy.copy(current_solution)
        new_solution[j] = 1 
        new_utility = compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u)
        new_cost = cost_function(new_solution, cost_vector)
        b = np.array([j])
        search_set = np.setdiff1d(search_set,b)
#         print(search_set)
#         search_set = np.delete(search_set,j)
#         print(current_solution)
        
        if new_cost <= B:
            current_solution = copy.copy(new_solution)
#             print([int(i) for i in current_solution])
            current_utility = new_utility
            current_cost = new_cost
            
            
    print('Greedy Approach \n'+ 'Utility: ' + str(current_utility))# + '\n' + 'Cost: ' + str(current_cost))
    
    return current_solution, current_utility, current_cost, select_set




def acyclic_greedy_alg_2(g_f, y_p, y_f, Y_p, Y_f, solution, cost_vector, u, B):
    n = len(solution)
    current_utility = compute_utility(y_p, y_f, Y_p, Y_f, solution, u)
    current_cost=cost_function(solution, cost_vector)
    Selected_appliances = []
    Selected_Super_nodes = []
    final_sol = [0]*n


    g_f_reduced_2, Super_nodes = make_acyclic_scc(g_f)
    Cost_of_Super_nodes = Super_Costs(Super_nodes,cost_vector)
    Utility_of_Super_nodes = Super_Utilities(Super_nodes,u)

    L = len(Super_nodes)
    y_f2 = bsf_depend_vector_2(g_f_reduced_2, L)
    Y_f2 = successors_number(y_f2)
    search_set = np.arange(L)
    
    current_solution = np.zeros(L)
    for i in range(L):
        select_set=list()
        A=list()
        for l in search_set:
            temp_solution = copy.copy(current_solution)
            temp_solution[l]=1
            Potential_appliances = []
            x_temp = [0]*n
            for k in range(L):
                if temp_solution[k]:
                    Potential_appliances.extend(Super_nodes[list(Super_nodes.keys())[k]])
            for k in range(n):
                if k in Potential_appliances:
                    x_temp[k] = 1
#             ll = compute_utility(y_p, y_f, Y_p, Y_f, x_temp, u)/ cost_function(x_temp, cost_vector)
#             ll = compute_utility(y_p, y_f, Y_p, Y_f, x_temp, u)/ Cost_of_Super_nodes[l]
            ll = compute_utility(y_p, y_f, Y_p, Y_f, x_temp, u)/ (Cost_of_Super_nodes[l]+sum(y_f2[l]*list(Cost_of_Super_nodes.values())))
#             ll = compute_utility(y_p, y_f, Y_p, Y_f, x_temp, u)
            select_set.append((ll, l))

        A=sorted(select_set, reverse=True)
        j = A[0][1]
#         print('j='+str(j))
        new_solution = copy.copy(current_solution)
        new_solution = np.logical_or(new_solution, y_f2[j])*1
        new_solution[j] = 1
        Potential_appliances = []
        x = [0]*n
        for k in range(L):
            if new_solution[k]:
                Potential_appliances.extend(Super_nodes[list(Super_nodes.keys())[k]])
        for k in range(n):
            if k in Potential_appliances:
                x[k] = 1
        new_utility = compute_utility(y_p, y_f, Y_p, Y_f, x, u)
        new_cost = cost_function(x, cost_vector)
        
        b = np.array([j])
        search_set = np.setdiff1d(search_set,b)
#         print(search_set)
#         search_set = np.delete(search_set,j)
#         print(current_solution)
        
        if new_cost <= B:
            current_solution = copy.copy(new_solution)
#             print([int(i) for i in current_solution])
            current_utility = new_utility
            current_cost = new_cost
            final_sol = x
                

    
    print('Acyclic Greedy Approach \n'+ 'Utility: ' + str(current_utility))# + '\n' + 'Cost: ' + str(current_cost))
#     return Super_nodes, Cost_of_Super_nodes, g_fr_inverse, Selected_appliances, Selected_Super_nodes
    return final_sol, current_utility, current_cost


def acyclic_greedy_alg(g_f, y_p, y_f, Y_p, Y_f, solution, cost_vector, u, B):    # zero outdegree
    n = len(solution)
    current_utility = compute_utility(y_p, y_f, Y_p, Y_f, solution, u)
    current_cost=cost_function(solution, cost_vector)
    Selected_appliances = []
    Selected_Super_nodes = []
    final_sol = [0]*n


    g_f_reduced_2, Super_nodes = make_acyclic_scc(g_f)
    Cost_of_Super_nodes = Super_Costs(Super_nodes,cost_vector)
    Utility_of_Super_nodes = Super_Utilities(Super_nodes,u)

    L = len(Super_nodes)
    y_f2 = bsf_depend_vector_2(g_f_reduced_2, L)
    Y_f2 = successors_number(y_f2)
    # search_set = np.arange(L)
    G = copy.copy(g_f_reduced_2)

    current_solution = np.zeros(L)
    for i in range(L):
        out_d = list(G.out_degree())
    #     print('out_d = '+str(out_d))
        zero_out_d = []
        for i in range(len(out_d)):
            if out_d[i][1]==0:
                zero_out_d.append(out_d[i][0])
        search_set = copy.copy(zero_out_d)
    #     print('search_set = '+str(search_set))

        select_set = list()
        A=list()
        for l in search_set:
            temp_solution = copy.copy(current_solution)
            temp_solution[l]=1
            Potential_appliances = []
            x_temp = [0]*n
            for k in range(L):
                if temp_solution[k]:
                    Potential_appliances.extend(Super_nodes[list(Super_nodes.keys())[k]])
            for k in range(n):
                if k in Potential_appliances:
                    x_temp[k] = 1
            ll = compute_utility(y_p, y_f, Y_p, Y_f, x_temp, u)/ (Cost_of_Super_nodes[l])
            select_set.append((ll, l))

        A=sorted(select_set, reverse=True)
    #     print('A = '+str(A))
        j = A[0][1]
    #     print('j = '+str(j))
        new_solution = copy.copy(current_solution)
    #     new_solution = np.logical_or(new_solution, y_f2[j])*1
        new_solution[j] = 1
        Potential_appliances = []
        x = [0]*n
        for k in range(L):
            if new_solution[k]:
                Potential_appliances.extend(Super_nodes[list(Super_nodes.keys())[k]])
        for k in range(n):
            if k in Potential_appliances:
                x[k] = 1
        new_utility = compute_utility(y_p, y_f, Y_p, Y_f, x, u)
        new_cost = cost_function(x, cost_vector)

    #     b = np.array([j])
    #     search_set = np.setdiff1d(search_set,b)

        if new_cost <= B:
    #         print('Yes! Picked '+str(Super_nodes[j]))
            current_solution = copy.copy(new_solution)
    #         print([int(i) for i in current_solution])
            current_utility = new_utility
            current_cost = new_cost
            final_sol = x
            G.remove_node(j)
    
    print('CODY \n'+ 'Utility: ' + str(current_utility))# + '\n' + 'Cost: ' + str(current_cost))
#     return Super_nodes, Cost_of_Super_nodes, g_fr_inverse, Selected_appliances, Selected_Super_nodes
    return final_sol, current_utility, current_cost


# n = 30             #nodes_number
# p = 0.3            #probability


# # random wattage energy list
# rand_cost = random_energy(n)
# # random utility array
# rand_utility = random_utility(n)
# # maximum utility of the current graph 
# current_max_utility = sum(rand_utility)

# # for b in range_budget():
# # it creates one random graph
# g = new_random_graph(n, p)

# # this function create another graph (functional graph) from the graph g
# funct_g, pref_g = two_graphs(g)     

# # compute the dependencies arrays 
# y_p = depend_vector(pref_g)       
# y_f = bsf_depend_vector(funct_g, n)    
# Y_p = successors_number(y_p)
# Y_f = successors_number(y_f)


# sol = list(np.zeros(n))
# B = 40000

# # current_solution, current_utility, current_cost, select_set = greedy_alg(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, B)

# # Appliances = list(np.where(current_solution))
# # Appliances = [x+1 for x in Appliances]

# # print('Greedy Approach \n Solution: ' + str(current_solution) + '\n' + 'Utility: ' + str(current_utility) + '\n' + 'Cost: ' + str(current_cost))

# # print('Appliances: ' + str(Appliances))


# # # # Super_nodes, Cost_of_Super_nodes, g_fr_inverse, Selected_appliances,Selected_Super_nodes = acyclic_greedy_alg(funct_g, y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, B)

# Acyclic_solution, Acyclic_utility, Acyclic_cost= acyclic_greedy_alg(funct_g, y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, B)
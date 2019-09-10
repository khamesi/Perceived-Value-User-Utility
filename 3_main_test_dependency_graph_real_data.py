# -*- coding: utf-8 -*-


import pandas as pd
from main_functions import *    
from graph import create_graph, depend_vector, successors_number, bsf_depend_vector
from milp import *
from random_graphs import * 
import random
import numpy as np
from save_plot import *
from sim_annealing import simulated_annealing, modified_simulated_annealing
import matplotlib.pyplot as plt


"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^ REAL graphs ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
# lista nodi con relativi valori di watt e utility
df = pd.read_csv('real_appliances/appliances_list.csv', sep = ',')
# df = pd.read_csv('real_appliances/appliances_list_with_fridge_freezer.csv', sep = ',')
#my_index_list = list(df['index'])
my_nodes_list = list(df['id'])

#number of appliances
n = len(my_nodes_list)

my_energy_list = list(df['energy'])
my_utility_list = list(df['utility'])
knapsack_utility_list = list(df['knapsack_utility'])

my_range = [800, 1000, 1200]
# my_range = [800, 2700, 2800]

""" GRAFO REALE
"""
# directed graphs 
fg = nx.DiGraph()
pg = nx.DiGraph()
appliance_dict={}
appliance_index = 0

# add nodes
for i in my_nodes_list:
    fg.add_node(i)
    pg.add_node(i)

f_df = pd.read_csv('real_appliances/Dependency_Graph.csv', sep = ',')    
# f_df = pd.read_csv('real_appliances/Dependency_Graph_with_fridge_freezer.csv', sep = ',')    
# p_df = pd.read_csv('real_appliances/preference_graph.csv', sep = ',')    


for i in f_df.iterrows():    
    x = i[1]
    fg.add_edge(x['Source'], x['Target'])
    
Appliance_dict={}
for i in range(n):
    Appliance_dict[my_nodes_list[i]] = i
func_g = nx.relabel_nodes(fg, Appliance_dict, copy=True)

y_p = depend_vector(pg)
y_f = bsf_depend_vector(func_g, n)   

Y_p = successors_number(y_p)
Y_f = successors_number(y_f)


nx.draw(func_g,with_labels=True)

reduced, Super_nodes = make_acyclic_scc(fg)
# print(str(Super_nodes))
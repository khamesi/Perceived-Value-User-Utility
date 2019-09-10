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


# my_range = [30, 130, 390 ]
# my_range = [6000, 14000, 22000]
# my_range = [30, 130, 390, 6000, 14000, 22000]
# my_range = [6000, 7500, 8000]
# my_range = [12000, 14000, 15000]
# my_range = [22000, 24000, 25000]
# my_range = [14000, 22000, 25000]
my_range = [6000,9000,19000]

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
#     appliance_dict[appliance_index]= i
#     fg.add_node(appliance_index)
#     pg.add_node(appliance_index)
#     appliance_index+=1

f_df = pd.read_csv('real_appliances/Dependency_Graph.csv', sep = ',')    
# f_df = pd.read_csv('real_appliances/Dependency_Graph_with_fridge_freezer.csv', sep = ',')    
# p_df = pd.read_csv('real_appliances/preference_graph.csv', sep = ',')    


for i in f_df.iterrows():    
    x = i[1]
    fg.add_edge(x['Source'], x['Target'])
   
# for i in p_df.iterrows():    
#     y = i[1]
#     pg.add_edge(y['Source'], y['Target'])
#     fg.add_edge(y['Source'], y['Target'])
    

Appliance_dict={}
# index = 0
for i in range(n):
    Appliance_dict[my_nodes_list[i]] = i
#     index+=1
func_g = nx.relabel_nodes(fg, Appliance_dict, copy=True)

y_p = depend_vector(pg)
y_f = bsf_depend_vector(func_g, n)   

Y_p = successors_number(y_p)
Y_f = successors_number(y_f)


MILP_real_list, KNAPSACK_real_list, GREEDY_real_list, ACYCLIC_GREEDY_real_list, milp_real_sol, knap_real_sol, greedy_real_solution, Acyclic_real_solution = real_graphs_case(my_range,func_g, y_p, y_f, Y_p, Y_f, my_energy_list, my_utility_list, knapsack_utility_list, n)


# convert lists into arrays to compute division
max_utilities_array = np.array(sum(my_utility_list))
max_knapsack_utilities_array = np.array(sum(knapsack_utility_list))
y_array_MILP = np.array(MILP_real_list)
y_array_KNAPSACK = np.array(KNAPSACK_real_list)
y_array_GREEDY = np.array(GREEDY_real_list)
y_array_ACYCLIC_GREEDY = np.array(ACYCLIC_GREEDY_real_list)

# compute the percentage utility
final_y_MILP = 100 * (y_array_MILP / max_utilities_array)
final_y_KNAPSACK = 100 * (y_array_KNAPSACK / max_utilities_array)
# final_y_KNAPSACK = 100 * (y_array_KNAPSACK / max_knapsack_utilities_array)
final_y_GREEDY = 100 * (y_array_GREEDY / max_utilities_array)
final_y_ACYCLIC_GREEDY = 100 * (y_array_ACYCLIC_GREEDY / max_utilities_array)


# convert array into list
final_y_MILP = list(final_y_MILP)
final_y_KNAPSACK = list(final_y_KNAPSACK)
final_y_GREEDY = list(final_y_GREEDY)
final_y_ACYCLIC_GREEDY = list(final_y_ACYCLIC_GREEDY)
# final_y_ACYCLIC_GREEDY[2]=final_y_KNAPSACK[2]
# final_y_KNAPSACK[2]=final_y_ACYCLIC_GREEDY[1]


n_groups = len(my_range)
# means_frank = MILP_real_list
# means_guido = ACYCLIC_GREEDY_real_list
 
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.15
opacity = 1
 
rects1 = plt.bar(index- .5*bar_width, final_y_MILP, bar_width,
                 alpha=opacity,
                 color='b',
                 label='OPT')
 
rects2 = plt.bar(index + .5*bar_width, final_y_ACYCLIC_GREEDY, bar_width,
                 alpha=opacity,
                 color='g',
                 label='CODY')

rects3 = plt.bar(index + 1.5*bar_width, final_y_GREEDY, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Greedy')

rects4 = plt.bar(index + 2.5*bar_width, final_y_KNAPSACK, bar_width,
                 alpha=opacity,
                 color='k',
                 label='knapsack')
 
plt.xlabel('Budget')
plt.ylabel('% Utility')
# plt.title('Scores by person')
plt.xticks(index + bar_width, (str(my_range[0]), str(my_range[1]),str(my_range[2])))
# plt.xticks(index + bar_width, (str(my_range[0]), str(my_range[1]),str(my_range[2]),str(my_range[3]),str(my_range[4]),str(my_range[5])))
plt.legend()
# plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
 
plt.tight_layout()
plt.show()
fig.savefig('real_appliances//Figs//real_plot' + '.eps', dpi=100)
fig.savefig('real_appliances//Figs//real_plot' + '.png', dpi=100)
fig.savefig('real_appliances//Figs//real_plot' + '.jpg', dpi=100)
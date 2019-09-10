# -*- coding: utf-8 -*-
import pandas as pd
import csv
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
# list of Appliances and correscponding Energy and Utility
# df = pd.read_csv('Real Field Experiment/User_1_utility_list.csv', sep = ',')
# df = pd.read_csv('Real Field Experiment/User_2_utility_list.csv', sep = ',')
# df = pd.read_csv('Real Field Experiment/User_2_utility_list_2.csv', sep = ',')
df = pd.read_csv('Real Field Experiment/User_3_utility_list.csv', sep = ',')

# f_df = pd.read_csv('Real Field Experiment/User_1_dependency.csv', sep = ',')    
# f_df = pd.read_csv('Real Field Experiment/User_1_dependency_ORIG.csv', sep = ',')    
# f_df = pd.read_csv('Real Field Experiment/User_2_dependency.csv', sep = ',')  
# f_df = pd.read_csv('Real Field Experiment/User_2_dependency_2.csv', sep = ',')  
# f_df = pd.read_csv('Real Field Experiment/User_2_dependency_ORIG.csv', sep = ',')    
f_df = pd.read_csv('Real Field Experiment/User_3_dependency.csv', sep = ',') 
my_nodes_list = list(df['Appliance'])

#number of appliances
n = len(my_nodes_list)

my_energy_list = list(df['energy_2'])
CODY_utility_list = list(df['utility'])
knapsack_utility_list = list(df['knapsack_utility'])


#Energy Budget
my_range = [130,650,850,2750,4500,5500,6000,8000,19000]
# my_range = [4500,5500,6000,8000]
# my_range = list(range(8000,19000,500))
# my_range = [19000]


""" Real Graph
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



for i in f_df.iterrows():    
    x = i[1]
    fg.add_edge(x['Source'], x['Target'])
       

Appliance_dict={}
# index = 0
for i in range(n):
    Appliance_dict[my_nodes_list[i]] = i
#     index+=1
func_g = nx.relabel_nodes(fg, Appliance_dict, copy=True)
func_p = nx.relabel_nodes(pg, Appliance_dict, copy=True)

y_p = depend_vector(pg)
y_f = bsf_depend_vector(func_g, n)   

Y_p = successors_number(y_p)
Y_f = successors_number(y_f)

diff_E_Q=list()
diff_E_L=list()

MILP_list = []

for index in range(len(my_range)):
    b = my_range[index]
    sol = list(np.zeros(n))
    print('Budget = '+str(b)+'\n')



    CODY_real_field_solution, CODY_real_field_utility, CODY_real_field_cost= acyclic_greedy_alg(func_p, y_p, y_f, Y_p, Y_f, sol, my_energy_list, CODY_utility_list, b)
    
    Cody_appliance=list()
    for i in range(n):
        if CODY_real_field_solution[i]==1:
            Cody_appliance.append(list(Appliance_dict.keys())[i])
        Cody_appliance.sort()
    print('Cody_appliance: \n' + str(Cody_appliance)+'\n')
    
    Cody_appliance.insert(0,str(b))
    Cody_appliance.insert(1,'Cody')
    Cody_appliance.insert(2,str(CODY_real_field_utility))
    with open('Real Field Experiment/App Lists/User 3.csv', "a",encoding="utf-8") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(Cody_appliance)
    
    
#     CODY_no_dependency_solution, CODY_no_dependency_utility, CODY_no_dependency_cost= acyclic_greedy_alg(func_p, y_p, y_f, Y_p, Y_f, sol, my_energy_list, CODY_utility_list, b) #(func_g, y_p, y_p, Y_p, Y_p, sol, my_energy_list, CODY_utility_list, b)
    
#     Cody_no_dependency_appliance=list()
#     for i in range(n):
#         if CODY_no_dependency_solution[i]==1:
#             Cody_no_dependency_appliance.append(list(Appliance_dict.keys())[i])
#     print('Cody_no_dependency_appliance: \n' + str(Cody_no_dependency_appliance)+'\n')



    m_milp, milp_sol = complete_milp(y_p, y_f, Y_p, Y_f, my_energy_list, b, CODY_utility_list, n)            
    MILP_appliance=list()
    for i in range(n):
        if milp_sol[i]==1:
            MILP_appliance.append(list(Appliance_dict.keys())[i])
        MILP_appliance.sort()
    print('MILP_appliance: \n' + str(MILP_appliance)+'\n')
    
    MILP_appliance.insert(0,str(b))
    MILP_appliance.insert(1,'MILP')
    MILP_appliance.insert(2,str(m_milp.objVal))
    with open('Real Field Experiment/App Lists/User 3.csv', "a",encoding="utf-8") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(MILP_appliance)
 

    knapsack_utility, m, knap_real_sol = knapsack_2(y_p, y_f, Y_p, Y_f, my_energy_list, b, knapsack_utility_list, CODY_utility_list, n)
    
    knapsack_appliance=list()
    for i in range(n):
        if knap_real_sol[i]==1:
            knapsack_appliance.append(list(Appliance_dict.keys())[i])
        knapsack_appliance.sort()
    print('knapsack_appliance: \n' + str(knapsack_appliance)+'\n')
    
#     print('\n')
    
    knapsack_appliance.insert(0,str(b))
    knapsack_appliance.insert(1,'knapsack')
    knapsack_appliance.insert(2,str(knapsack_utility))
    with open('Real Field Experiment/App Lists/User 3.csv', "a",encoding="utf-8") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(knapsack_appliance)
        
        
    Greedy_solution, Greedy_utility, Greedy_cost, sorted_select_set = greedy_alg_knapsack(y_p, y_f, Y_p, Y_f, sol, my_energy_list, CODY_utility_list,knapsack_utility_list, b)
    
    Greedy_appliance=list()
    for i in range(n):
        if Greedy_solution[i]==1:
            Greedy_appliance.append(list(Appliance_dict.keys())[i])
        Greedy_appliance.sort()
    print('knapsack_appliance: \n' + str(Greedy_appliance)+'\n')
    
    print('\n')
    
    Greedy_appliance.insert(0,str(b))
    Greedy_appliance.insert(1,'Greedy')
    Greedy_appliance.insert(2,str(Greedy_utility))
    with open('Real Field Experiment/App Lists/User 3.csv', "a",encoding="utf-8") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(Greedy_appliance)
    

    
# Cody_appliance.insert(0,str(b))
# Cody_appliance.insert(1,'Cody')
# with open('Real Field Experiment/App Lists/test.csv', "w", encoding="utf-8") as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerow(Cody_appliance)
# Appliance_dict = pd.DataFrame(my_range, columns=['Budget'])
# Appliance_dict['CODY Appliances'] = Cody_appliance
# Appliance_dict['knapsack Appliances'] = knapsack_appliance

# Appliance_dict.to_csv('Real Field Experiment/App Lists/test.csv',float_format='%.3f', header= True, index=False)

 
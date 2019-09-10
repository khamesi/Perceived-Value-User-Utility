# -*- coding: utf-8 -*-
"""
Modified on Thu Sep 28 2018 By Atieh

"""

import pandas as pd
from main_functions import *    
from graph import create_graph, depend_vector, successors_number, bsf_depend_vector
from milp import *
from random_graphs import * 
import random
import numpy as np
from save_plot import *

"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^ERDOS RENYI random graphs ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Networkx library has some functions about it
y = utility
"""
random.seed(a = 1)

"""
INCREASING PROBABILITY [ 0 (knapsack) to 0.9 ]
"""

x_prob, y_prob_MILP, y_prob_SIM, y_prob_MODSIM, y_prob_KNAPSACK, y_prob_GREEDY, y_prob_ACYCLIC_GREEDY, sigma_prob_MILP, sigma_prob_SIM, sigma_prob_MODSIM,sigma_prob_KNAPSACK, sigma_prob_GREEDY, sigma_prob_ACYCLIC_GREEDY, iter_prob_SIM, iter_prob_MODSIM = probability_case()
# create a dataframe from the dictionary and save it as csv file
MILP_prob_dict = pd.DataFrame(x_prob, columns=['m'])
MILP_prob_dict['Utility'] = y_prob_MILP
MILP_prob_dict['standard deviation'] = sigma_prob_MILP

SIM_prob_dict = pd.DataFrame(x_prob, columns=['m'])
SIM_prob_dict['Utility'] = y_prob_SIM
SIM_prob_dict['standard deviation'] = sigma_prob_SIM

# MODSIM_prob_dict = pd.DataFrame(x_prob, columns=['m'])
# MODSIM_prob_dict['Utility'] = y_prob_MODSIM
# MODSIM_prob_dict['standard deviation'] = sigma_prob_MODSIM

KNAPSACK_prob_dict = pd.DataFrame(x_prob, columns=['m'])
KNAPSACK_prob_dict['Utility'] = y_prob_KNAPSACK
KNAPSACK_prob_dict['standard deviation'] = sigma_prob_KNAPSACK

GREEDY_prob_dict = pd.DataFrame(x_prob, columns=['m'])
GREEDY_prob_dict['Utility'] = y_prob_GREEDY
GREEDY_prob_dict['standard deviation'] = sigma_prob_GREEDY

ACYCLIC_GREEDY_prob_dict = pd.DataFrame(x_prob, columns=['m'])
ACYCLIC_GREEDY_prob_dict['Utility'] = y_prob_ACYCLIC_GREEDY
ACYCLIC_GREEDY_prob_dict['standard deviation'] = sigma_prob_ACYCLIC_GREEDY


SIM_prob_iter = pd.DataFrame(x_prob, columns=['m'])
SIM_prob_iter['itr'] = iter_prob_SIM
# MODSIM_prob_iter = pd.DataFrame(x_prob, columns=['m'])
# MODSIM_prob_iter['itr'] = iter_prob_MODSIM

# save the csv files
MILP_prob_dict.to_csv('random_graphs_data/prob_MILP.csv',float_format='%.3f', header= True, index=False)
SIM_prob_dict.to_csv('random_graphs_data/prob_SIM.csv',float_format='%.3f', header= True, index=False)
# MODSIM_prob_dict.to_csv('random_graphs_data/prob_MODSIM.csv',float_format='%.3f', header= True, index=False)
KNAPSACK_prob_dict.to_csv('random_graphs_data/prob_KNAPSACK.csv',float_format='%.3f', header= True, index=False)
GREEDY_prob_dict.to_csv('random_graphs_data/prob_GREEDY.csv',float_format='%.3f', header= True, index=False)
ACYCLIC_GREEDY_prob_dict.to_csv('random_graphs_data/prob_ACYCLIC_GREEDY.csv',float_format='%.3f', header= True, index=False)

# iterations results about the probability used for each condition 
SIM_prob_iter.to_csv('random_graphs_data/iter_prob_SIM.csv',float_format='%.3f', header= True, index=False)
# MODSIM_prob_iter.to_csv('random_graphs_data/iter_prob_MODSIM.csv',float_format='%.3f', header= True, index=False)

##############################################################################################################################


# """ 
# INCREASING NUMBER OF NODES ( 10 to 40 ) 
# """
# x_nodes, y_nodes_MILP, y_nodes_SIM, y_nodes_MODSIM, y_nodes_KNAPSACK, y_nodes_GREEDY, y_nodes_ACYCLIC_GREEDY, sigma_nodes_MILP, sigma_nodes_SIM, sigma_nodes_MODSIM, sigma_nodes_KNAPSACK, sigma_nodes_GREEDY, sigma_nodes_ACYCLIC_GREEDY, iter_nodes_SIM, iter_nodes_MODSIM  = nodes_case()
# # create a dataframe from the dictionary and save it as csv file
# MILP_nodes_dict = pd.DataFrame(x_nodes, columns=['Nodes'])
# MILP_nodes_dict['Utility'] = y_nodes_MILP
# MILP_nodes_dict['standard deviation'] = sigma_nodes_MILP

# SIM_nodes_dict = pd.DataFrame(x_nodes, columns=['Nodes'])
# SIM_nodes_dict['Utility'] = y_nodes_SIM
# SIM_nodes_dict['standard deviation'] = sigma_nodes_SIM

# # MODSIM_nodes_dict = pd.DataFrame(x_nodes, columns=['Nodes'])
# # MODSIM_nodes_dict['Utility'] = y_nodes_MODSIM
# # MODSIM_nodes_dict['standard deviation'] = sigma_nodes_MODSIM

# KNAPSACK_nodes_dict = pd.DataFrame(x_nodes, columns=['Nodes'])
# KNAPSACK_nodes_dict['Utility'] = y_nodes_KNAPSACK
# KNAPSACK_nodes_dict['standard deviation'] = sigma_nodes_KNAPSACK

# GREEDY_nodes_dict = pd.DataFrame(x_nodes, columns=['Nodes'])
# GREEDY_nodes_dict['Utility'] = y_nodes_GREEDY
# GREEDY_nodes_dict['standard deviation'] = sigma_nodes_GREEDY

# ACYCLIC_GREEDY_nodes_dict = pd.DataFrame(x_nodes, columns=['Nodes'])
# ACYCLIC_GREEDY_nodes_dict['Utility'] = y_nodes_ACYCLIC_GREEDY
# ACYCLIC_GREEDY_nodes_dict['standard deviation'] = sigma_nodes_ACYCLIC_GREEDY

# SIM_nodes_iter = pd.DataFrame(x_nodes, columns=['Nodes'])
# SIM_nodes_iter['itr'] = iter_nodes_SIM
# # MODSIM_nodes_iter = pd.DataFrame(x_nodes, columns=['Nodes'])
# # MODSIM_nodes_iter['itr'] = iter_nodes_MODSIM

# # #save the csv files
# MILP_nodes_dict.to_csv('random_graphs_data/nodes_MILP.csv',float_format='%.3f', header= True, index=False)
# SIM_nodes_dict.to_csv('random_graphs_data/nodes_SIM.csv' ,float_format='%.3f', header= True, index=False)
# # MODSIM_nodes_dict.to_csv('random_graphs_data/nodes_MODSIM.csv',float_format='%.3f', header= True, index=False)
# KNAPSACK_nodes_dict.to_csv('random_graphs_data/nodes_KNAPSACK.csv',float_format='%.3f', header= True, index=False)
# GREEDY_nodes_dict.to_csv('random_graphs_data/nodes_GREEDY.csv',float_format='%.3f', header= True, index=False)
# ACYCLIC_GREEDY_nodes_dict.to_csv('random_graphs_data/nodes_ACYCLIC_GREEDY.csv',float_format='%.3f', header= True, index=False)

# SIM_nodes_iter.to_csv('random_graphs_data/iter_nodes_SIM.csv' ,float_format='%.3f', header= True, index=False)
# # MODSIM_nodes_iter.to_csv('random_graphs_data/iter_nodes_MODSIM.csv',float_format='%.3f', header= True, index=False)

# #############################################################################################################################

# """ 
# INCREASING BUDGET  ( from 15.000 to 150.000)
# """

# x_budget, y_budget_MILP, y_budget_SIM, y_budget_MODSIM, y_budget_KNAPSACK, y_budget_GREEDY, y_budget_ACYCLIC_GREEDY, sigma_budget_MILP, sigma_budget_SIM, sigma_budget_MODSIM, sigma_budget_KNAPSACK, sigma_budget_GREEDY, sigma_budget_ACYCLIC_GREEDY, iter_budget_SIM, iter_budget_MODSIM  = budget_case()
# # create a dataframe from the dictionary and save it as csv file
# MILP_budget_dict = pd.DataFrame(x_budget, columns=['Budget'])
# MILP_budget_dict['Utility'] = y_budget_MILP
# MILP_budget_dict['standard deviation'] = sigma_budget_MILP

# SIM_budget_dict = pd.DataFrame(x_budget, columns=['Budget'])
# SIM_budget_dict['Utility'] = y_budget_SIM
# SIM_budget_dict['standard deviation'] = sigma_budget_SIM

# # MODSIM_budget_dict = pd.DataFrame(x_budget, columns=['Budget'])
# # MODSIM_budget_dict['Utility'] = y_budget_MODSIM
# # MODSIM_budget_dict['standard deviation'] = sigma_budget_MODSIM

# KNAPSACK_budget_dict = pd.DataFrame(x_budget, columns=['Budget'])
# KNAPSACK_budget_dict['Utility'] = y_budget_KNAPSACK
# KNAPSACK_budget_dict['standard deviation'] = sigma_budget_KNAPSACK

# GREEDY_budget_dict = pd.DataFrame(x_budget, columns=['Budget'])
# GREEDY_budget_dict['Utility'] = y_budget_GREEDY
# GREEDY_budget_dict['standard deviation'] = sigma_budget_GREEDY

# ACYCLIC_GREEDY_budget_dict = pd.DataFrame(x_budget, columns=['Budget'])
# ACYCLIC_GREEDY_budget_dict['Utility'] = y_budget_ACYCLIC_GREEDY
# ACYCLIC_GREEDY_budget_dict['standard deviation'] = sigma_budget_ACYCLIC_GREEDY

# SIM_budget_iter = pd.DataFrame(x_budget, columns=['Budget'])
# SIM_budget_iter['itr'] = iter_budget_SIM
# # MODSIM_budget_iter = pd.DataFrame(x_budget, columns=['Budget'])
# # MODSIM_budget_iter['itr'] = iter_budget_MODSIM

# # # save the csv files
# MILP_budget_dict.to_csv('random_graphs_data/budget_MILP.csv', float_format='%.3f', header= True, index=False)
# SIM_budget_dict.to_csv('random_graphs_data/budget_SIM.csv', float_format='%.3f', header= True, index=False)
# # MODSIM_budget_dict.to_csv('random_graphs_data/budget_MODSIM.csv',float_format='%.3f', header= True, index=False)
# KNAPSACK_budget_dict.to_csv('random_graphs_data/budget_KNAPSACK.csv',float_format='%.3f', header= True, index=False)
# GREEDY_budget_dict.to_csv('random_graphs_data/budget_GREEDY.csv',float_format='%.3f', header= True, index=False)
# ACYCLIC_GREEDY_budget_dict.to_csv('random_graphs_data/budget_ACYCLIC_GREEDY.csv',float_format='%.3f', header= True, index=False)

# SIM_budget_iter.to_csv('random_graphs_data/iter_budget_SIM.csv',float_format='%.3f', header= True, index=False)
# # MODSIM_budget_iter.to_csv('random_graphs_data/iter_budget_MODSIM.csv',float_format='%.3f', header= True, index=False)


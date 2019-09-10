# -*- coding: utf-8 -*-
"""
PRINCIPAL FUNCTIONS

@author: dolcev
"""

import pandas as pd
import numpy as np
import scipy.optimize as spopt
import networkx.algorithms.traversal as nt
import networkx.algorithms.connectivity as nc
from threshold import thresholding
from usage_probability import absolute_prob    
from usage_probability import joint_prob
from usage_probability import cond_prob
from graph import *
from configuration import *
from random_graphs import *
from myknapsack import *

"""
constant parameters
"""
nodes_number = 30
budget = 30000
m = 5
samples_number = 300

"""
creating sample number
"""
def sample_number():
    
    N = 20
    
    return N

"""
WEEKLY AVERAGE FOR EACH DEVICE
"""
def calculate_weekly_avg():
    for f in folder_list:
        res, out = weekly_avg(output_folder, f)
    
    return res, out
    

"""
 ABOSULUTE PROBABILITIES OF EACH DEVICE FOR EACH HOUR
"""
def calculate_abs_prob():
    threshold_dic = {}    # to fill with thresholoded values

    # create an empty dictioraty to fill with all absolute probability for each device and for each hour
    abs_prob = {}
    i = 0
    
    for i in range( len(folder_list) ):
        # thresholing to binarize the wattage in each time slot
        threshold_dic[folder_list[i]] = thresholding(output_folder, folder_list[i], threshold_list[i])
        
        # calculate the absolute probability for each hour (prob is passed-by-reference)
        absolute_prob(threshold_dic[folder_list[i]], abs_prob, folder_list[i])
        
    return threshold_dic, abs_prob
    
"""
CONDITIONAL PROBABILITY for ALL POSSIBLE couples of devices
""" 
def calculate_cond_prob(abs_prob, threshold_dic):
    """
    JOINT PROBABILITIES FOR COUPLES OF DEVICES
    
    PART 1 : calculate the logical and between each couple of devices (no repetitive)
             for each minute
    
    
    PART 2 : calculate the joint probability for each couple of devices 
             using the same function to calculate the absolute probability
             It's just a statistic approach (number_value_true/60)
             
    #"""
    # empty list for couples of devices
    l = []
    
    # create a list with the name of columns for the joint_prob
    # ex. Alarmclock_&_Coffeemaker, Alarmclock_&_Dishwasher
    for i in range(len(folder_list)-1):
        j=i
        for j in range(i + 1, len(folder_list)):       
            l.append(folder_list[i]+ '_&_' + folder_list[j])
           
    
    # calculate the joint probability like absolute probability for each hour
    j_prob = pd.DataFrame(index=range(total_rows), columns=l)
    
    joint_prob(threshold_dic, folder_list, output_folder, j_prob)
        
    """
    CONDITIONAL PROBABILITY for ALL POSSIBLE couples of devices
    
    create a DICTIONARY with all devices. 
    For each device A, I have a Dataframe that holds all 
    conditional probabilities p(A!B), p(A!C).. like columns
    """
    
    # dictionary for the list of each device with all other devices except the current device
    # I need these lists to give the name to the columns of Dataframe for each device
    device_dic = {}
    i = 0
    for i in range(len(folder_list)):
        device_dic[folder_list[i]] = folder_list[:i] + folder_list[i + 1 :]
    
    
    # empty dictionary for all Dataframe conditional probabilities
    cond_prob_dictionary = {}
    
    for f in folder_list:
         # create a Dataframe for each device to fill in with all conditional probability 
         # ex. p(A|B) , p(A|C), p(A|D) ... they are included inside a Dataframe
         cond_prob_dictionary['condit_prob_%02s' % f] = pd.DataFrame(index=range(total_rows), columns=device_dic[f])
         
                
    cond_prob(folder_list, abs_prob, j_prob, cond_prob_dictionary)
    
    # save the csv file with the conditional probabilities for each device
    for f in folder_list:
        cond_prob_dictionary['condit_prob_' + f].to_csv(output_folder + f +'_cond_prob.csv', sep=';', float_format='%.3f', header= True, index=False)
    
    return j_prob, cond_prob_dictionary
    

"""
 check if all elements in list1 are in list2
 and return a flag True or False
"""
def check_list(list1, list2):
    flag = False
        
    for l in list1:
            if (l in list2) == True:
                flag = True
            else:
                flag = False
                break
    return flag

    
"""
ERDOS RENYI random graphs
1) KNAPSACK
2) MILP
3) SIMULATED ANNEALING
"""
def probability_case():    
    """   ********* INCREASING PROBABILITY (0 to 0.9)  ********** """
    print('increasing probability')
    
#     # constant parameters
#     nodes_number = 30
#     budget = 30000
#     samples_number = sample_number()
# #     Num = len(range_probability())
    Num = len(range_m(nodes_number))
    
    y_prob_MILP = {} # dictionary
    y_prob_SIM = {} # dictionary
    y_prob_MODSIM = {} # dictionary
    y_prob_KNAPSACK = {} # dictionary
    y_prob_GREEDY = {} # dictionary
    y_prob_ACYCLIC_GREEDY = {} # dictionary
    
    iter_SIM = {}
    iter_MODSIM = {}

    # total sum of all samples utilities,empty array with length=10 because of 0 to 0.9
    y_tot_prob_MILP = np.zeros(Num)    
    y_tot_prob_SIM = np.zeros(Num)    
    y_tot_prob_MODSIM = np.zeros(Num)    
    y_tot_prob_KNAPSACK = np.zeros(Num)    
    y_tot_prob_GREEDY = np.zeros(Num)    
    y_tot_prob_ACYCLIC_GREEDY = np.zeros(Num)    
    
    #iterations average
    iter_tot_SIM = np.zeros(Num)    
    iter_tot_MODSIM = np.zeros(Num) 

   ## to get 100 samples
    for i in range(samples_number):
        x_prob, y_prob_MILP[i], y_prob_SIM[i], y_prob_MODSIM[i], y_prob_KNAPSACK[i], y_prob_GREEDY[i], y_prob_ACYCLIC_GREEDY[i], iter_SIM[i], iter_MODSIM[i] = random_probability_graphs(nodes_number, budget)
        # add the previus list to the total array 
        y_tot_prob_MILP = y_tot_prob_MILP + y_prob_MILP[i]
        y_tot_prob_SIM = y_tot_prob_SIM + y_prob_SIM[i]
        y_tot_prob_MODSIM = y_tot_prob_MODSIM + y_prob_MODSIM[i]
        y_tot_prob_KNAPSACK = y_tot_prob_KNAPSACK + y_prob_KNAPSACK[i]
        y_tot_prob_GREEDY = y_tot_prob_GREEDY + y_prob_GREEDY[i]
        y_tot_prob_ACYCLIC_GREEDY = y_tot_prob_ACYCLIC_GREEDY + y_prob_ACYCLIC_GREEDY[i]

        # sum of iterations
        iter_tot_SIM = iter_tot_SIM + iter_SIM[i]
        iter_tot_MODSIM = iter_tot_MODSIM + iter_MODSIM[i]

       
    # to compute the mean values of utility, divide by 100 because I got 100 sample
    mean_y_prob_MILP = y_tot_prob_MILP/samples_number
    mean_y_prob_SIM = y_tot_prob_SIM/samples_number
    mean_y_prob_MODSIM = y_tot_prob_MODSIM/samples_number
    mean_y_prob_KNAPSACK = y_tot_prob_KNAPSACK/samples_number
    mean_y_prob_GREEDY = y_tot_prob_GREEDY/samples_number
    mean_y_prob_ACYCLIC_GREEDY = y_tot_prob_ACYCLIC_GREEDY/samples_number
    
    mean_iter_SIM = iter_tot_SIM/samples_number
    mean_iter_MODSIM = iter_tot_MODSIM/samples_number
    
    sum_MILP = 0
    sum_SIM = 0
    sum_MODSIM = 0
    sum_KNAPSACK = 0
    sum_GREEDY = 0
    sum_ACYCLIC_GREEDY = 0
    
    for i in range(samples_number):
        pow_MILP = pow(y_prob_MILP[i] - mean_y_prob_MILP , 2)
        pow_SIM = pow(y_prob_SIM[i] - mean_y_prob_SIM , 2)
        pow_MODSIM = pow(y_prob_MODSIM[i] - mean_y_prob_MODSIM , 2)
        pow_KNAPSACK = pow(y_prob_KNAPSACK[i] - mean_y_prob_KNAPSACK , 2)
        pow_GREEDY = pow(y_prob_GREEDY[i] - mean_y_prob_GREEDY , 2)
        pow_ACYCLIC_GREEDY = pow(y_prob_ACYCLIC_GREEDY[i] - mean_y_prob_ACYCLIC_GREEDY , 2)
        sum_MILP = sum_MILP + pow_MILP
        sum_SIM = sum_SIM + pow_SIM
        sum_MODSIM = sum_MODSIM + pow_MODSIM
        sum_KNAPSACK = sum_KNAPSACK + pow_KNAPSACK
        sum_GREEDY = sum_GREEDY + pow_GREEDY
        sum_ACYCLIC_GREEDY = sum_ACYCLIC_GREEDY + pow_ACYCLIC_GREEDY
        
    sigma_MILP = np.sqrt(sum_MILP)/samples_number
    sigma_SIM = np.sqrt(sum_SIM)/samples_number
    sigma_MODSIM = np.sqrt(sum_MODSIM)/samples_number
    sigma_KNAPSACK = np.sqrt(sum_KNAPSACK)/samples_number
    sigma_GREEDY = np.sqrt(sum_GREEDY)/samples_number
    sigma_ACYCLIC_GREEDY = np.sqrt(sum_ACYCLIC_GREEDY)/samples_number
    # convert into integer
#    mean_iter_SIM = mean_iter_SIM.astype(int)
#    mean_iter_MODSIM = mean_iter_MODSIM.astype(int)

#     # print plots
#     string = 'Nodes Number = ' + str(nodes_number)+'\n'+ 'Budget = ' + str(budget)
#     xy_plot2(x_prob, mean_y_prob_MILP, mean_y_prob_SIM,'MILP & SIMULATED ANNEALING \n Increasing Probability \n ' + string, 'Probability', '% Utility', 'Milp', 'Sim.Ann', 'random_graphs_data\mean_increasing_prob_plot')

    # create a dataframe from the dictionary and save it as csv file
#    y_prob_dict_MILP = pd.DataFrame(y_prob_MILP)
#    y_prob_dict_SIM = pd.DataFrame(y_prob_SIM)
#    y_prob_dict_MILP.to_csv('random_graphs_data\y_prob_MILP.csv',orient='rows' ,float_format='%.3f', header= True, index=False)
#    y_prob_dict_SIM.to_csv('random_graphs_data\y_prob_MILP.csv',orient='rows' ,float_format='%.3f', header= True, index=False)
    return x_prob, mean_y_prob_MILP, mean_y_prob_SIM, mean_y_prob_MODSIM, mean_y_prob_KNAPSACK, mean_y_prob_GREEDY, mean_y_prob_ACYCLIC_GREEDY, sigma_MILP, sigma_SIM, sigma_MODSIM, sigma_KNAPSACK, sigma_GREEDY, sigma_ACYCLIC_GREEDY, mean_iter_SIM, mean_iter_MODSIM
    
    
"""   ********* INCREASING NODES NUMBER (20 to 200) ********** """
def nodes_case():
    print('increasing nodes number')
#     # constant parameters
# #     probability = 0.3
#     m = 3
#     budget = 30000    # la somma di tutti i costi di 100 nodi e' 140.000
#     samples_number = sample_number()
    Num = len(range_nodes())
    
    # dictionaries
    y_nodes_MILP = {} 
    y_nodes_SIM = {} 
    y_nodes_MODSIM = {} 
    y_nodes_KNAPSACK = {}
    y_nodes_GREEDY = {}
    y_nodes_ACYCLIC_GREEDY = {}

    # iterations dicts
    iter_SIM = {}
    iter_MODSIM = {}

    
    y_tot_nodes_MILP = np.zeros(Num)    # enmpty array, its length of y is 10 ( 10 steps from 10 to 100)
    y_tot_nodes_SIM = np.zeros(Num)
    y_tot_nodes_MODSIM = np.zeros(Num)
    y_tot_nodes_KNAPSACK = np.zeros(Num)
    y_tot_nodes_GREEDY = np.zeros(Num)
    y_tot_nodes_ACYCLIC_GREEDY = np.zeros(Num)
    
    #iterations average
    iter_tot_SIM = np.zeros(Num)    
    iter_tot_MODSIM = np.zeros(Num) 
    
    
    for i in range(samples_number):
        x_nodes, y_nodes_MILP[i], y_nodes_SIM[i], y_nodes_MODSIM[i], y_nodes_KNAPSACK[i], y_nodes_GREEDY[i], y_nodes_ACYCLIC_GREEDY[i], iter_SIM[i], iter_MODSIM[i] = random_nodes_graphs(m, budget) 
        y_tot_nodes_MILP = y_tot_nodes_MILP + y_nodes_MILP[i]
        y_tot_nodes_SIM = y_tot_nodes_SIM + y_nodes_SIM[i]
        y_tot_nodes_MODSIM = y_tot_nodes_MODSIM + y_nodes_MODSIM[i]
        y_tot_nodes_KNAPSACK = y_tot_nodes_KNAPSACK + y_nodes_KNAPSACK[i]
        y_tot_nodes_GREEDY = y_tot_nodes_GREEDY + y_nodes_GREEDY[i]
        y_tot_nodes_ACYCLIC_GREEDY = y_tot_nodes_ACYCLIC_GREEDY + y_nodes_ACYCLIC_GREEDY[i]

        # sum of iterations
        iter_tot_SIM = iter_tot_SIM + iter_SIM[i]
        iter_tot_MODSIM = iter_tot_MODSIM + iter_MODSIM[i]        
           
    # to compute the mean of 100 samples of each number of nodes
    mean_y_nodes_MILP = y_tot_nodes_MILP/samples_number
    mean_y_nodes_SIM = y_tot_nodes_SIM/samples_number
    mean_y_nodes_MODSIM = y_tot_nodes_MODSIM/samples_number
    mean_y_nodes_KNAPSACK = y_tot_nodes_KNAPSACK/samples_number
    mean_y_nodes_GREEDY = y_tot_nodes_GREEDY/samples_number
    mean_y_nodes_ACYCLIC_GREEDY = y_tot_nodes_ACYCLIC_GREEDY/samples_number
    
    # compute the mean iterations of 100 samples
    mean_iter_SIM = iter_tot_SIM/samples_number
    mean_iter_MODSIM = iter_tot_MODSIM/samples_number
    
    sum_MILP = 0
    sum_SIM = 0
    sum_MODSIM = 0
    sum_KNAPSACK = 0
    sum_GREEDY = 0
    sum_ACYCLIC_GREEDY = 0
    
    for i in range(samples_number):
        pow_MILP = pow(y_nodes_MILP[i] - mean_y_nodes_MILP , 2)
        pow_SIM = pow(y_nodes_SIM[i] - mean_y_nodes_SIM , 2)
        pow_MODSIM = pow(y_nodes_MODSIM[i] - mean_y_nodes_MODSIM , 2)
        pow_KNAPSACK = pow(y_nodes_KNAPSACK[i] - mean_y_nodes_KNAPSACK , 2)
        pow_GREEDY = pow(y_nodes_GREEDY[i] - mean_y_nodes_GREEDY , 2)
        pow_ACYCLIC_GREEDY = pow(y_nodes_ACYCLIC_GREEDY[i] - mean_y_nodes_ACYCLIC_GREEDY , 2)
        sum_MILP = sum_MILP + pow_MILP
        sum_SIM = sum_SIM + pow_SIM
        sum_MODSIM = sum_MODSIM + pow_MODSIM
        sum_KNAPSACK = sum_KNAPSACK + pow_KNAPSACK
        sum_GREEDY = sum_GREEDY + pow_GREEDY
        sum_ACYCLIC_GREEDY = sum_ACYCLIC_GREEDY + pow_ACYCLIC_GREEDY
    
    sigma_MILP = np.sqrt(sum_MILP)/samples_number
    sigma_SIM = np.sqrt(sum_SIM)/samples_number
    sigma_MODSIM = np.sqrt(sum_MODSIM)/samples_number
    sigma_KNAPSACK = np.sqrt(sum_KNAPSACK)/samples_number
    sigma_GREEDY = np.sqrt(sum_GREEDY)/samples_number
    sigma_ACYCLIC_GREEDY = np.sqrt(sum_ACYCLIC_GREEDY)/samples_number
    
    
    ##to create the plot
    #string = 'Probability = 0.5 \n' + 'Budget = 70000 '
    #xy_plot2(x_nodes, mean_y_nodes_MILP,mean_y_nodes_SIM, 'MILP & SIMULATED ANNEALING \n Increasing Nodes Number ( BFS )\n' + string, 'Nodes', '% Utility','Milp', 'Sim.Ann', 'random_graphs_data\increasing_nodes_plot')
    
    # create a dataframe from the dictionary and save it as csv file
#    y_nodes_dict = pd.DataFrame(y_nodes)
#    y_nodes_dict.to_csv('random_graphs_data\y_nodes_list.csv',orient='rows' ,float_format='%.3f', header= True, index=False)
    return x_nodes, mean_y_nodes_MILP, mean_y_nodes_SIM, mean_y_nodes_MODSIM, mean_y_nodes_KNAPSACK, mean_y_nodes_GREEDY, mean_y_nodes_ACYCLIC_GREEDY, sigma_MILP, sigma_SIM, sigma_MODSIM, sigma_KNAPSACK, sigma_GREEDY, sigma_ACYCLIC_GREEDY, mean_iter_SIM, mean_iter_MODSIM

    
"""   ********* INCREASING BUDGET ********** """
def budget_case():
    print('increasing budget')
#     # constant parameters
#     nodes_number = 30
# #     probability = 0.3
#     m = 3
#     samples_number = sample_number()
    Num = len(range_budget())
    
    
    # dictionaries to store utility values
    y_budget_MILP = {} 
    y_budget_SIM = {}
    y_budget_MODSIM = {}
    y_budget_KNAPSACK = {}
    y_budget_GREEDY = {}
    y_budget_ACYCLIC_GREEDY = {}

    # number of iterations
    iter_SIM = {}
    iter_MODSIM = {}

    y_tot_budget_MILP = np.zeros(Num)   # empty array, its length is 10 (10 different budget values)
    y_tot_budget_SIM = np.zeros(Num)
    y_tot_budget_MODSIM = np.zeros(Num)
    y_tot_budget_KNAPSACK = np.zeros(Num)
    y_tot_budget_GREEDY = np.zeros(Num)
    y_tot_budget_ACYCLIC_GREEDY = np.zeros(Num)
    
    #iterations average
    iter_tot_SIM = np.zeros(Num)    
    iter_tot_MODSIM = np.zeros(Num) 
    
    
    for i in range(samples_number):
        x_budget, y_budget_MILP[i], y_budget_SIM[i], y_budget_MODSIM[i],y_budget_KNAPSACK[i], y_budget_GREEDY[i], y_budget_ACYCLIC_GREEDY[i], iter_SIM[i], iter_MODSIM[i] = random_budget_graphs(nodes_number, m)
        y_tot_budget_MILP = y_tot_budget_MILP + y_budget_MILP[i]
        y_tot_budget_SIM = y_tot_budget_SIM + y_budget_SIM[i]
        y_tot_budget_MODSIM = y_tot_budget_MODSIM + y_budget_MODSIM[i]
        y_tot_budget_KNAPSACK = y_tot_budget_KNAPSACK + y_budget_KNAPSACK[i]
        y_tot_budget_GREEDY = y_tot_budget_GREEDY + y_budget_GREEDY[i]
        y_tot_budget_ACYCLIC_GREEDY = y_tot_budget_ACYCLIC_GREEDY + y_budget_ACYCLIC_GREEDY[i]
        # sum of iterations
        iter_tot_SIM = iter_tot_SIM + iter_SIM[i]
        iter_tot_MODSIM = iter_tot_MODSIM + iter_MODSIM[i]

        
    # to compute the mean value of each sample (number of devices)
    mean_y_budget_MILP = y_tot_budget_MILP/samples_number
    mean_y_budget_SIM = y_tot_budget_SIM/samples_number
    mean_y_budget_MODSIM = y_tot_budget_MODSIM/samples_number
    mean_y_budget_KNAPSACK = y_tot_budget_KNAPSACK/samples_number
    mean_y_budget_GREEDY = y_tot_budget_GREEDY/samples_number
    mean_y_budget_ACYCLIC_GREEDY = y_tot_budget_ACYCLIC_GREEDY/samples_number
    
    mean_iter_SIM = iter_tot_SIM/samples_number
    mean_iter_MODSIM = iter_tot_MODSIM/samples_number
    
    # for errors bars
    sum_MILP = 0
    sum_SIM = 0
    sum_MODSIM = 0
    sum_KNAPSACK = 0
    sum_GREEDY = 0
    sum_ACYCLIC_GREEDY = 0
    
    for i in range(samples_number):
        pow_MILP = pow(y_budget_MILP[i] - mean_y_budget_MILP , 2)
        pow_SIM = pow(y_budget_SIM[i] - mean_y_budget_SIM , 2)
        pow_MODSIM = pow(y_budget_MODSIM[i] - mean_y_budget_MODSIM , 2)
        pow_KNAPSACK = pow(y_budget_KNAPSACK[i] - mean_y_budget_KNAPSACK , 2)
        pow_GREEDY = pow(y_budget_GREEDY[i] - mean_y_budget_GREEDY , 2)
        pow_ACYCLIC_GREEDY = pow(y_budget_ACYCLIC_GREEDY[i] - mean_y_budget_ACYCLIC_GREEDY , 2)
        sum_MILP = sum_MILP + pow_MILP
        sum_SIM = sum_SIM + pow_SIM
        sum_MODSIM = sum_MODSIM + pow_MODSIM
        sum_KNAPSACK = sum_KNAPSACK + pow_KNAPSACK
        sum_GREEDY = sum_GREEDY + pow_GREEDY
        sum_ACYCLIC_GREEDY = sum_ACYCLIC_GREEDY + pow_ACYCLIC_GREEDY
    
    sigma_MILP = np.sqrt(sum_MILP)/samples_number
    sigma_SIM = np.sqrt(sum_SIM)/samples_number
    sigma_MODSIM = np.sqrt(sum_MODSIM)/samples_number
    sigma_KNAPSACK = np.sqrt(sum_KNAPSACK)/samples_number
    sigma_GREEDY = np.sqrt(sum_GREEDY)/samples_number
    sigma_ACYCLIC_GREEDY = np.sqrt(sum_ACYCLIC_GREEDY)/samples_number
    
#     string = 'Probability = ' + str(probability) +'\n' + 'Nodes Number = ' + str(nodes_number)
#     xy_plot2(x_budget, mean_y_budget_MILP, mean_y_budget_SIM,'MILP & SIMULATED ANNEALING \n with Increasing Budget\n' + string, 'Budget', '% Utility', 'Milp', 'Sim.Ann','random_graphs_data\increasing_budget_plot')

    ### create a dataframe from the dictionary and save it as csv file
    #y_budget_dict = pd.DataFrame(y_budget_MILP)
    #y_budget_dict.to_csv('random_graphs_data\y_budget_list.csv',orient='rows' ,float_format='%.3f', header= True, index=False)
    return x_budget, mean_y_budget_MILP, mean_y_budget_SIM, mean_y_budget_MODSIM, mean_y_budget_KNAPSACK, mean_y_budget_GREEDY, mean_y_budget_ACYCLIC_GREEDY, sigma_MILP, sigma_SIM, sigma_MODSIM, sigma_KNAPSACK, sigma_GREEDY, sigma_ACYCLIC_GREEDY, mean_iter_SIM, mean_iter_MODSIM
    
    

def real_graphs_case(my_range, funct_g, y_p, y_f, Y_p, Y_f, my_energy_list, my_utility_list, knapsack_utility_list, n):
    samples_number = 1
    
    sol = list(np.zeros(n))

    MILP_list = []
    KNAPSACK_list = []
    GREEDY_list = []
    ACYCLIC_GREEDY_list = []
    MODSA_list = []
    SA_list = []
    
    # error bars
    sigma_SA = []
    sigma_MODSA = []
    
    for b in my_range:
        print('Budget = '+str(b))
        """ MILP """
        m_milp, milp_sol = complete_milp(y_p, y_f, Y_p, Y_f, my_energy_list, b, my_utility_list, n)            
        # to get the objective function value (AXIS Y)
        obj = m_milp.getObjective()
        MILP_list.append(obj.getValue())   
    
        """KNAPSACK"""
#         knapsack_utility, m, knap_sol = knapsack(y_p, y_f, Y_p, Y_f, my_energy_list, b, my_utility_list, n)
        knapsack_utility, m, knap_sol = knapsack_2(y_p, y_f, Y_p, Y_f, my_energy_list, b, knapsack_utility_list, my_utility_list, n)
#         KNAPSACK_list.append(knapsack_utility)     
        
#         knapsack_utility, knap_sol = new_knapsack(y_p, y_f, Y_p, Y_f, my_energy_list, b, my_utility_list, n)
#         knapsack_utility, knap_sol = new_knapsack_2(y_p, y_f, Y_p, Y_f, my_energy_list, b, my_utility_list, knapsack_utility_list, n) 
        KNAPSACK_list.append(knapsack_utility)
                
        
               
        """  ******* GREEDY  ********  """
#         print('greedy')
        greedy_solution, greedy_utility, greedy_cost, sorted_select_set = greedy_alg(y_p, y_f, Y_p, Y_f, sol, my_energy_list, my_utility_list, b)
#         greedy_solution, greedy_utility, greedy_cost = acyclic_greedy_alg_2(funct_g, y_p, y_f, Y_p, Y_f, sol, my_energy_list, my_utility_list, b)
        GREEDY_list.append(greedy_utility)
 
        
        """  ******* ACYCLIC GREEDY  ********  """
#         print('acyclic greedy')
        Acyclic_solution, Acyclic_utility, Acyclic_cost= acyclic_greedy_alg(funct_g, y_p, y_f, Y_p, Y_f, sol, my_energy_list, my_utility_list, b)
        ACYCLIC_GREEDY_list.append(Acyclic_utility)

        
        
#         samples_SA = []
#         samples_MODSA = []
    
#         sum_SA = 0
#         sum_MODSA = 0
        
        
#         for i in range(samples_number):    
#             """SIMULATED ANNEALING"""
#             sol = list(np.zeros(n))   
#             solution, u_val, iterations = simulated_annealing(y_p, y_f, Y_p, Y_f, sol, my_energy_list, my_utility_list, b)
#             samples_SA.append(u_val)
#             sum_SA = sum_SA + u_val
            
#             """ SMART SIMULATED ANNEALING"""    
#             sol = list(np.zeros(n))     
#             solution, u_val, iterations = modified_simulated_annealing(y_p, y_f, Y_p, Y_f, sol, my_energy_list, my_utility_list, b)
#             samples_MODSA.append(u_val)
#             sum_MODSA = sum_MODSA + u_val
            
#         # average of samples
#         avg_SA = sum_SA/samples_number
#         avg_MODSA = sum_MODSA/samples_number    
    
#         # average value of the current budget 
#         SA_list.append(avg_SA)
#         MODSA_list.append(avg_MODSA)
        
#         #errors bar
#         sum_SA = 0
#         sum_MODSA = 0
        
#         for i in range(samples_number):
#             pow_SA = pow(samples_SA[i] - avg_SA , 2)
#             pow_MODSA = pow(samples_MODSA[i] - avg_MODSA , 2)
#             sum_SA = sum_SA + pow_SA
#             sum_MODSA = sum_MODSA + pow_MODSA        
        
#         sigma_SA.append( np.sqrt(sum_SA)/samples_number)
#         sigma_MODSA.append( np.sqrt(sum_MODSA)/samples_number)
        
    return MILP_list, KNAPSACK_list, GREEDY_list, ACYCLIC_GREEDY_list, milp_sol, knap_sol, greedy_solution, Acyclic_solution
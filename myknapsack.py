import pandas as pd
import numpy as np
import copy

from functools import lru_cache

def knapsack_dyn_prog(total_nodes, budget, energy_list, utility_list, y_p, y_f, Y_p, Y_f ):

    #variables
    #will eventually calculate total_nodes and max_energy from list input
#    total_nodes = 30
    
    #will be user input
#    budget = 4000
                      
    #list of nodes with energy and value
    #input total nodes
#    path = 'nodeslist.csv'
#    df = pd.read_csv(path, sep = ',')
#    
#    energy_list = list(df['Energy'])
#    utility_list = list(df['Utility'])                 
    #sets values of nodes_list for 0-29
#    nodes_list = list(range(total_nodes))
#    budget_list = list(range(budget))
    
    #Creates a table of max energy by total nodes
    Table = pd.DataFrame(0, index=range(total_nodes + 1), columns=range(budget + 1))
         
    for i in range(total_nodes):
        i = i +1
        for j in range(budget):
            j = j + 1
#             print(j)
            if i>0 and j>0:       
                if energy_list[i - 1] > j:
    
                    Table[j][i] = Table[j][i - 1]
                else:
                    if (j - energy_list[i - 1]) >= 0 and (utility_list[i - 1] + Table[j - energy_list[i - 1]][i - 1]) > Table[j][i- 1]:
                        Table[j][i] = utility_list[i - 1] + Table[j - energy_list[i - 1]][i - 1]
                    else:
                        Table[j][i] = Table[j][i - 1]
    
#     print('table ready')
    
    ###Creates an array to store binary answer of which nodes were selected
    Answer = list(np.zeros(total_nodes + 1))    # the first element is always 0
    i = total_nodes #temporary variable to track node number
    j = budget  #temporary variable to track total energy
    total_energy = 0 
    #total_utility = 0 
    
    while (i>0 and j>0):
#         print(i)
        if j - energy_list[i - 1] >= 0 and Table[j][i] == utility_list[i - 1] + Table[j -energy_list[i - 1]][i - 1]:
            Answer[i]=1
            j = j-energy_list[i - 1]
            #total_utility = total_utility + utility_list[i - 1]
            total_energy = total_energy + energy_list[i - 1]
        i = i - 1     
     
    # compute the final utility considering dependencies
    total_utility = compute_utility(y_p, y_f, Y_p, Y_f, Answer[1:], utility_list)
        
    
    print('knapsack cost: ' + str(total_energy))
    print('knapsack utility: ' + str(total_utility))
    
    return Answer, total_utility
    
    
"""
Compute the utility for one subset x and the info about graph dependencies
u = utility array
"""
def compute_utility(y_p, y_f, Y_p, Y_f, solution, u):
    
    alpha = 1
    
    x = np.array(solution, dtype = bool )
    
    l = np.size(x)
    z_p = np.zeros(l)
    z_f = np.zeros(l, dtype = bool)    
    
    # get a copy of the list x
    my_x = copy.copy(x)
    
    for i in range(l):
        if my_x[i] == True:        
            # functional variable
            if Y_f[i] != 0: # if xi has some dependencies
                z_f_val = sum (my_x * y_f[i])/ Y_f[i]
            else:
                z_f_val = 1 # xi has no dependencies
            
            if z_f_val == 1.0 : # otherwise zf and zp will be still zero
                z_f[i] = True # all functional dependencies all satisfied
                if Y_p[i] != 0 : # to avoid division by zero
                    z_p[i] = sum (z_f * y_p[i])/ Y_p[i]
                else:
                    z_p[i] = 1 # if xi has no preference dependencies
        #i = i + 1
    # now we have z_p and z_f vector to compute the utility
    final_utility =  sum(u * z_f) 
    
    return final_utility




def knapsack_test(items, maxweight):
    """Solve the knapsack problem by finding the most valuable subsequence
    of items that weighs no more than maxweight.

    items must be a sequence of pairs (value, weight), where value is a
    number and weight is a non-negative integer.

    maxweight is a non-negative integer.

    Return a pair whose first element is the sum of values in the most
    valuable subsequence, and whose second element is the subsequence.

    >>> items = [(4, 12), (2, 1), (6, 4), (1, 1), (2, 2)]
    >>> knapsack(items, 15)
    (11, [(2, 1), (6, 4), (1, 1), (2, 2)])

    """
    @lru_cache(maxsize=None)
    def bestvalue(i, j):
        # Return the value of the most valuable subsequence of the first
        # i elements in items whose weights sum to no more than j.
        if j < 0:
            return float('-inf')
        if i == 0:
            return 0
        value, weight = items[i - 1]
        return max(bestvalue(i - 1, j), bestvalue(i - 1, j - weight) + value)

    j = maxweight
    result = []
    for i in reversed(range(len(items))):
        if bestvalue(i + 1, j) != bestvalue(i, j):
            result.append(items[i])
            j -= items[i][1]
    result.reverse()
    return bestvalue(len(items), maxweight), result


def new_knapsack(y_p, y_f, Y_p, Y_f, my_energy_list, b, my_utility_list, n):
    items = []
    for i in range(n):
    #     print(i)
        items.append((i,my_energy_list[i]))
    #     items[i]=(i,my_energy_list[i])
    aa, result = knapsack_test(items, b)
    temp = 0
    # my_sol = np.zeros(n)
    my_sol = [0]*n

    for i in range(len(result)):
        temp = temp + result[i][1]
        my_sol[result[i][0]] = 1
    # print(temp)
    # print(my_sol)

    my_knap_utility = compute_utility(y_p, y_f, Y_p, Y_f, my_sol, my_utility_list)
    
    return my_knap_utility, my_sol

def new_knapsack_2(y_p, y_f, Y_p, Y_f, my_energy_list, b, my_utility_list, knapsack_utility_list, n):
    items = []
    for i in range(n):
    #     print(i)
        items.append((i,my_energy_list[i]))
    #     items[i]=(i,my_energy_list[i])
    aa, result = knapsack_test(items, b)
    temp = 0
    # my_sol = np.zeros(n)
    my_sol = [0]*n

    for i in range(len(result)):
        temp = temp + result[i][1]
        my_sol[result[i][0]] = 1
    # print(temp)
    # print(my_sol)

    my_knap_utility = compute_utility(y_p, y_f, Y_p, Y_f, my_sol, my_utility_list)
    
    return my_knap_utility, my_sol
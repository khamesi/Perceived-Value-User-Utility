# -*- coding: utf-8 -*-
"""
SIMULATED ANNEALING algorithm

@author: dolcev
"""
import numpy as np
import random
import scipy.optimize
from configuration  import *
from graph import depend_vector, bsf_depend_vector, successors_number
import copy
import math

"""
SIMULATED ANNEALING
the function receive the first random solution that will be optimize.
it's a binary vector of appliances
"""
def simulated_annealing(y_p, y_f, Y_p, Y_f, solution, cost_vector, u, B):
    
    current_solution = copy.copy(solution)
       
    # compute the utility value of the current solution
    old_utility = compute_utility(y_p, y_f, Y_p, Y_f, current_solution, u)
    

    T = 1.0
    T_min = 0.0001
    coeff = 0.90     # if 0.9 we have 110 iterations
    count = 1   # counter
    stop_loop = 0
    iterations = 0
    x = []
    y = []
    while T > T_min :        
        i = 1        
        while i <= 50:

            
            # add or remove an appliance from my subset to get a neighbor state
            #new_solution = new_state(current_solution, cost_vector, B)
            new_solution = new_state(current_solution, cost_vector, B)

            # compute the new solution's utility
            new_utility = compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u)

            #compute the acceptance probability 
            ap = acceptance_probability(old_utility, new_utility, T)

            # if TRUE, switch the solutio   n with the new state
            if ap > random.random():
                # update the new solution
                current_solution = new_solution
                old_utility = new_utility
                stop_loop = 0   # into this if statement the current solution changes

            i = i + 1            
            count = count + 1

            x.append(count)
            y.append(old_utility)
            
            # stop the loop if we have the same solution for 1000 times in a row
            if stop_loop < 1000:
                stop_loop = stop_loop + 1 
                iterations = count

        T = T * coeff

    iterations = iterations - 999
    # SE DEVO FARE IL CONFRONTO CON LE DUE VERSIONI DEL SIMULATED ANNEALING
    # DEVO FARE RITORNARE I VETTORI X E Y
    print('Regulaer SA \nUtility:  ' + str(old_utility))
    
    return  current_solution, old_utility, iterations
    #return x, y, iterations
    
"""
SMART SIMULATED ANNEALING (SSA)
Modified version of SA
the function receive the NULL solution that will be optimize.
it's a binary vector of appliances
"""

def modified_simulated_annealing(y_p, y_f, Y_p, Y_f, solution, cost_vector, u, B):
    
    current_solution = copy.copy(solution)
    
    # compute the utility value of the current solution
    old_utility = compute_utility(y_p, y_f, Y_p, Y_f, current_solution, u)
    T = 1.0
    T_min = 0.0001
    coeff = 0.95     # if 0.9 we have 110 iterations
    count = 1   # counter
    stop_loop = 0   # to stop the loop after 1000 times in a row where the solution is the same
    x = []
    y = []
    
    best_solution = solution
    best_utility = old_utility
    iteration_best_solution = count

    while T > T_min and stop_loop <= 300:        
        i = 1       
        if stop_loop >= 300:
            break 
        while i <= 100:

            # add or remove an appliance from my subset to get a neighbor state            
            new_solution = new_state2(current_solution, u, cost_vector, B, y_p, y_f, Y_p, Y_f)
            #new_solution = new_state3(current_solution, u, cost_vector, B, y_p, y_f, Y_p, Y_f, T)
            # compute the new solution's utility
            new_utility = compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u)
               
            if new_utility > best_utility:
                best_solution = new_solution
                best_utility = new_utility
                iteration_best_solution = count
            
            
            #compute the acceptance probability 
            ap = acceptance_probability(best_utility, new_utility, T)
            #ap = acceptance_probability(cost_function(current_solution, cost_vector), cost_function(new_solution, cost_vector), T)
            # if TRUE, switch the solution with the new state
            if ap > random.random():
                if new_solution != current_solution:
                    stop_loop = 0
                current_solution = new_solution
                old_utility = new_utility
            
            i = i + 1
            count = count + 1    
            
            x.append(count)
            y.append(old_utility)
            
            # it's used to stop the loop if we have the same solution for 1000 times in a row
            stop_loop = stop_loop + 1

            
        T = T * coeff
    
#    if count >= 17999:
#        iterations = 18000
#    else:
    
    iterations = count - 299
    # SE DEVO FARE IL CONFRONTO CON LE DUE VERSIONI DEL SIMULATED ANNEALING
    # DEVO FARE RITORNARE I VETTORI X E Y
    print('Modified SA \n utility:  ' + str(old_utility))
    
    return best_solution, best_utility, iteration_best_solution
    
    #return  current_solution, old_utility,iterations 
    #return x, y, iterations

    
 

"""
compute the acceptance probability 
"""
def acceptance_probability(old_utility, new_utility, T):
    # exponent of the mathematical costant e
    exponent = (new_utility - old_utility)/ T

    return pow(np.e, exponent)
    
    
""" 
REGULAR VERSION
add or remove one element from the boolean vector x
the algorithm runs until it finds another solution that satisfies the budget limit
"""
def new_state(solution, cost_vector, B):

    flag = True
    while flag == True:
        # create a local variable of solution
        my_solution = copy.copy(solution)

        # select a randon value from 1 to N (vector dimension)
        rand_index = random.randint(0, np.size(my_solution) - 1)

        # insert the selected item
        my_solution[rand_index] = not my_solution[rand_index]
    
        # compute the utility of the new solution
        my_cost = cost_function(my_solution, cost_vector)
        #print('cost= ' + str(my_cost) + '   budget= ' + str(B)  )
        flag = my_cost > B
        # I found a feasible solution
        if flag == False:
            break
        
    return my_solution
            
    
"""
compute the cost of all appliaces into the subset
"""
def cost_function(x, c):
    my_x = np.array(x ,dtype = bool)    
    return sum(my_x * c)
        
"""
Compute the utility for one subset x and the info about graph dependencies
u = utility array
"""
def compute_utility(y_p, y_f, Y_p, Y_f, x, u):

    l = np.size(x)
    z_p = np.zeros(l)
    z_f = np.zeros(l, dtype = bool)  
    alpha = 1
    
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
#                     z_p[i] = sum (my_x * y_p[i])/ Y_p[i]
                    z_p[i] = sum (z_f * y_p[i])/ Y_p[i]
                else:
                    z_p[i] = 1 # if xi has no preference dependencies
        #i = i + 1
    # now we have z_p and z_f vector to compute the utility
    final_utility = (1 - alpha) * sum(u * z_p) +  alpha * sum(u * z_f) 
    
    return final_utility

    
"""
SPECIAL NEW_STATE FUNCTION
the new state is still random but it depends on dependencies 
If a node is added to the subtset, even its functional dependent appliances must be included
If a node is removed from the subset, even its functional dependent appliances must be removed
"""
def new_state2(solution, u, c, B, y_p, y_f, Y_p, Y_f):
    # generate a random boolean value with probability equal to 0.5 
    # to choose between to add or remove an appliance
    # flag = True -> add an appliance
    # flag = False -> remove an appliance
    flag = random.random() < 0.5
    # copy of the current solution
    current_solution = copy.copy(solution)

    current_utility = compute_utility(y_p, y_f, Y_p, Y_f, solution, u)
    current_cost = cost_function(solution, c)
    
    # boolean list of all dependent appliances of the current 
    dependent_devices = []
    # w list of 
    w = {}
    p = {} 
    j = 0 
    """ ADD an appliance and its dependent appliances"""
    if flag == True :
#        print('ADD')
        # create a dictionary
        for i in solution:
            if i == False:
                # index of the i-th element                
                #index = solution.index(i)
                index = j
                # boolean list of functional dependent appliances
                dependent_devices = y_f[index]         
                       
                # copy every time the initial solution                
                current_solution = copy.copy(solution)
                # add the i-th element
                current_solution[index] = not current_solution[index] 
                # LOGICAL OR to add functional dependent appliances of the i-th element
                new_solution = np.logical_or(current_solution, dependent_devices)
                new_solution = list(new_solution) 
                # comput the cost of the new solution to know if it meets the budget
                new_cost = cost_function(new_solution, c)
                
                if new_cost <= B:
                    # compute delta Energy and Budget
                    delta_u = compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u) - current_utility
                    delta_b = new_cost - current_cost
                    # compute the division
                    w[index] = delta_u/delta_b
            j = j + 1
            
        # compute the sum of w_i
        s = sum(w.values())
        
        # compute the probability for each possible solution
        for i in w:
            p[i] = w[i] / s
        

        # there is no a new solution with a new appliance which meets the budget, then it returns the current solution
        if len(p) == 0:
            return solution
        # create a dictionary with the sum of two probability in a row
        p2 = {}
        j = 0
        l = list(p.keys())
        
        for i in range(len(l)):
            if i == 0:
                p2[l[i]] = p[l[i]]
            else:
                p2[l[i]] = p2[l[i- 1]] + p[l[i]]
            
            
        # initialization of these variables to keep the values of difference and index
        r = random.random()
        
        # my_index will be the appliance's index more close to the random value r        
        my_index = 0
        
        for i in range(len(l)):
            if i == 0:
                if r >= 0 and r <= p2[l[i]]:
                    my_index = l[i]
            else:
                if r >= p2[ l[i- 1] ] and r <= p2[ l[i] ]:
                    my_index = l[i] # select the upper end
        

        # compute the new solution
        dependent_devices = y_f[my_index]
        current_solution = copy.copy(solution)
        current_solution[my_index] = not current_solution[my_index] 
        new_solution = np.logical_or(current_solution, dependent_devices)
        new_solution = list(new_solution) 
        
        return new_solution

    # REMOVE an appliance and its dependent appliances
    else:         
        for i in solution:
            # if an appliance is present into the set, I can remove otherwise I skip it
            if i == True:
                # index of the i-th element
                #index = solution.index(i)
                index = j
                # boolean list of functional dependent appliances
                dependent_devices = y_f[index]
                
                # copy every time the initial solution                
                current_solution = copy.copy(solution)
                # remove the i-th element
                current_solution[index] = not current_solution[index] 
                # remove functional dependent appliances of the i-th element
                not_array = np.logical_not(dependent_devices)
                new_solution = np.logical_and(current_solution, not_array)
                new_solution = list(new_solution)                

                # compute delta Energy and Budget
                delta_u = compute_utility(y_p, y_f, Y_p, Y_f, solution, u) - compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u)
                delta_b =  cost_function(solution, c) - cost_function(new_solution, c)
                # compute the division
                w[index] = delta_u/delta_b
            
            j = j + 1
        # compute the sum of w_i
        s = 0
        for i in w:
            s = s + w[i]
        
        # compute the probability for each possible solution
        for i in w:
            if s == 0:
                p[i] = 0
            else:
                p[i] = w[i] / s

        # if the current solution is an empty subset and there are no appliances to remove 
        if len(p) == 0:
            return solution

        # random selection of one among all possible solution
        r = random.random()
        my_index = 0
        l = list(p.keys())      
        
        # pick randomly the index of one new solution 
        for i in range(len(l)):
            if i == 0:
                if r >= 0 and r <= p[l[i]]:
                    my_index = l[i]
            else:
                if r >= p[ l[i- 1] ] and r <= p[ l[i] ]:
                    my_index = l[i] # select the upper end

        # compute the new solution
        dependent_devices = y_f[my_index]
        current_solution = copy.copy(solution)
        current_solution[my_index] = not current_solution[my_index] 
        not_array = np.logical_not(dependent_devices)
        new_solution = np.logical_and(current_solution, not_array)
        new_solution = list(new_solution)

        return new_solution
    
        
"""
remove case is different:
it removes at most n/2 appiances related to the temperature values
"""
def new_state3(solution, u, c, B, y_p, y_f, Y_p, Y_f, T):
    # generate a random boolean value with probability equal to 0.5 
    # to choose between to add or remove an appliance
    # flag = True -> add an appliance
    # flag = False -> remove an appliance
    flag = random.random() < 0.5
    # copy of the current solution
    current_solution = copy.copy(solution)

    current_utility = compute_utility(y_p, y_f, Y_p, Y_f, solution, u)
    current_cost = cost_function(solution, c)
    
    # boolean list of all dependent appliances of the current 
    dependent_devices = []
    # w list of 
    w = {}
    p = {} 
    j = 0 
    """ ADD an appliance and its dependent appliances"""
    if flag == True :
#        print('ADD')
        # create a dictionary
        for i in solution:
            if i == False:
                # index of the i-th element                
                #index = solution.index(i)
                index = j
                # boolean list of functional dependent appliances
                dependent_devices = y_f[index]         
                       
                # copy every time the initial solution                
                current_solution = copy.copy(solution)
                # add the i-th element
                current_solution[index] = not current_solution[index] 
                # LOGICAL OR to add functional dependent appliances of the i-th element
                new_solution = np.logical_or(current_solution, dependent_devices)
                new_solution = list(new_solution) 
                # comput the cost of the new solution to know if it meets the budget
                new_cost = cost_function(new_solution, c)
                
                if new_cost <= B:
                    # compute delta Energy and Budget
                    delta_u = compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u) - current_utility
                    delta_b = new_cost - current_cost
                    # compute the division
                    w[index] = delta_u/delta_b
            j = j + 1
            
        # compute the sum of w_i
        s = sum(w.values())
        
        # compute the probability for each possible solution
        for i in w:
            p[i] = w[i] / s
        

        # there is no a new solution with a new appliance which meets the budget, then it returns the current solution
        if len(p) == 0:
            return solution
        # create a dictionary with the sum of two probability in a row
        p2 = {}
        j = 0
        l = list(p.keys())
        
        for i in range(len(l)):
            if i == 0:
                p2[l[i]] = p[l[i]]
            else:
                p2[l[i]] = p2[l[i- 1]] + p[l[i]]
            
            
        # initialization of these variables to keep the values of difference and index
        r = random.random()
        
        # my_index will be the appliance's index more close to the random value r        
        my_index = 0
        
        for i in range(len(l)):
            if i == 0:
                if r >= 0 and r <= p2[l[i]]:
                    my_index = l[i]
            else:
                if r >= p2[ l[i- 1] ] and r <= p2[ l[i] ]:
                    my_index = l[i] # select the upper end
        

        # compute the new solution
        dependent_devices = y_f[my_index]
        current_solution = copy.copy(solution)
        current_solution[my_index] = not current_solution[my_index] 
        new_solution = np.logical_or(current_solution, dependent_devices)
        new_solution = list(new_solution) 
        
        return new_solution

    # REMOVE an appliance and its dependent appliances
    else:   
        # nodes number i can remove
        k_max = sum(solution)
        # at the beginning k is equal to k_max, after it decrease with the temperature T
        k = math.ceil(T * k_max)
        for i in solution:
            # if an appliance is present into the set, I can remove otherwise I skip it
            if i == True:
                # index of the i-th element
                #index = solution.index(i)
                index = j
                # boolean list of functional dependent appliances
                dependent_devices = y_f[index]
                
                # copy every time the initial solution                
                current_solution = copy.copy(solution)
                # remove the i-th element
                current_solution[index] = not current_solution[index] 
                # remove functional dependent appliances of the i-th element
                not_array = np.logical_not(dependent_devices)
                new_solution = np.logical_and(current_solution, not_array)
                new_solution = list(new_solution)                

                # compute delta Energy and Budget
                delta_u = compute_utility(y_p, y_f, Y_p, Y_f, solution, u) - compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u)
                delta_b =  cost_function(solution, c) - cost_function(new_solution, c)
                # compute the division
                w[index] = delta_u/delta_b
            
            j = j + 1
        # compute the sum of w_i
        s = 0
        for i in w:
            s = s + w[i]
        
        # compute the probability for each possible solution
        for i in w:
            if s == 0:
                p[i] = 0
            else:
                p[i] = w[i] / s

        # if the current solution is an empty subset and there are no appliances to remove 
        if len(p) == 0:
            return solution

        # random selection of one among all possible solution
        r = random.random()
        my_index = 0
        l = list(p.keys())      
        
        # pick randomly the index of one new solution         
        random.shuffle(l)
        appliances_number = random.randint(1,k)
        index_list = l[0 : appliances_number]        

        current_solution = copy.copy(solution)
        for i in index_list:                
            # compute the new solution
            dependent_devices = y_f[i]
            current_solution = copy.copy(current_solution)
            current_solution[my_index] = not current_solution[my_index] 
            not_array = np.logical_not(dependent_devices)
            new_solution = np.logical_and(current_solution, not_array)
            new_solution = list(new_solution)

        return new_solution
    

    
# """
# Greedy Algorithm
# """

# def greedy_alg(y_p, y_f, Y_p, Y_f, solution, cost_vector, u, B):
    
#     current_solution = copy.copy(solution)
    
#     # compute the utility value of the current solution
#     current_utility = compute_utility(y_p, y_f, Y_p, Y_f, current_solution, u)
#     current_cost=cost_function(current_solution, cost_vector)

# #     count = 1   # counter
# #     stop_loop = 0   # to stop the loop after 1000 times in a row where the solution is the same
#     x = []
#     y = []
    
# #     best_solution = solution
# #     best_utility = old_utility
# #     iteration_best_solution = count

#     for i in range(len(solution)):
#         select_set[i]=sum (u * y_f[i])/ sum (cost_vector * y_f[i])


#     for i in range(len(solution)):
#         # add or remove an appliance from my subset to get a neighbor state            
#         new_solution = new_state_greedy(current_solution, u, cost_vector, B, y_p, y_f, Y_p, Y_f)
#         new_utility = compute_utility(y_p, y_f, Y_p, Y_f, new_solution, u)
#         new_cost=cost_function(new_solution, cost_vector)
        
#         if new_cost <= B:
#             current_solution = new_solution
#             current_utility = new_utility
#             current_cost = new_cost
            
            
            
#             x.append(count)
#             y.append(old_utility)
            
            
#     print('Modified SA \n utility:  ' + str(old_utility))
    
#     return best_solution, best_utility, iteration_best_solution
    
#     #return  current_solution, old_utility,iterations 
#     #return x, y, iterations

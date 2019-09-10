# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:02:10 2017

@author: dolcev
"""
from gurobipy import *
from configuration import *
import copy
import numpy as np

def knapsack(y_p, y_f, Y_p, Y_f, c, b, u, length):
    
    r = range(length) 
    
    try:        
        # create a new model
        m = Model("my_total_milp")
        m.setParam( 'OutputFlag', False )
        
        # create variables x_i
        x = m.addVars(1, length, vtype= GRB.BINARY, name="x")
              
        # objective function FUNCTIONAL + PREFERANCE
        m.setObjective( sum( x[0,i] * u[i] for i in r) , GRB.MAXIMIZE)              
           
        # budget constraint
        m.addConstr( ( sum(x[0,i] * c[i] for i in r) <= b ), 'c2' )
        
        m.optimize()        
        
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
    
    list_x = []
    
    for i in m.getVars():
        list_x.append(i.X)        
    
    # computes total utility using out utility function
    total_utitily = compute_utility(y_p, y_f, Y_p, Y_f, list_x, u)
    print('Knapsack \n'+ 'Utility: ' + str(total_utitily))
    return total_utitily, m, list_x


def knapsack_2(y_p, y_f, Y_p, Y_f, c, b, u, u_ours, length):
    
    r = range(length) 
    
    try:        
        # create a new model
        m = Model("my_total_milp")
        m.setParam( 'OutputFlag', False )
        
        # create variables x_i
        x = m.addVars(1, length, vtype= GRB.BINARY, name="x")
              
        # objective function FUNCTIONAL + PREFERANCE
        m.setObjective( sum( x[0,i] * u[i] for i in r) , GRB.MAXIMIZE)              
           
        # budget constraint
        m.addConstr( ( sum(x[0,i] * c[i] for i in r) <= b ), 'c2' )
        
        m.optimize()        
        
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
    
    list_x = []
    
    for i in m.getVars():
        list_x.append(i.X)        
    
    # computes total utility using out utility function
    total_utitily = compute_utility(y_p, y_f, Y_p, Y_f, list_x, u_ours)
#     total_utitily = compute_utility(y_p, y_f, Y_p, Y_f, list_x, u)
    print('Knapsack \n'+ 'Utility: ' + str(total_utitily))
    return total_utitily, m, list_x



"""
Compute the utility for one subset x and the info about graph dependencies
u = utility array
"""
def compute_utility(y_p, y_f, Y_p, Y_f, solution, u):
    
    x = np.array(solution, dtype = bool )
    alpha = 1
    
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
#                     z_p[i] = sum (my_x * y_p[i])/ Y_p[i]
                    z_p[i] = sum (z_f * y_p[i])/ Y_p[i]
                else:
                    z_p[i] = 1 # if xi has no preference dependencies
        #i = i + 1
    # now we have z_p and z_f vector to compute the utility
    final_utility = (1 - alpha) * sum(u * z_p) +  alpha * sum(u * z_f) 
    
    return final_utility
    
    
    
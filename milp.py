# -*- coding: utf-8 -*-
"""
MIXED INTEGER LINEAR PROGRAMMING PROBLEM
using the GUROBI API this function solve the MILP problem 

z_i and x_i are variables

objective function: max U(x)= sum(z_i * u_i)

constraints:  x_i,z_i, y_ij = {0,1}
              z_i <= sum( x_j * yij /Y_i)
              z_i <= x_i 
              C(x) = c_i * x_i <= B 
              

@author: dolcev
"""

from gurobipy import *
from configuration import *
from graph import depend_vector, bsf_depend_vector, successors_number
  

"""
MILP PROBLEM 
the objective formula includes the functional part and the preference part
"""
def complete_milp(y_p, y_f, Y_p, Y_f, c, b, u, length):
        
    r = range(length)   
    
    # dictionary of vectors y_ij indexed with devices index
#    y_p = depend_vector(pref_g)
#    
#    #y_f = depend_vector(funct_g)
#    y_f = bsf_depend_vector(funct_g, 2)    # to compute dependent devices using the bsf algorithm
#    
#    # dictionary with the numbers of dependent devices for each device, indexed with devices index (Alarmclock=0, ...)
#    Y_p = successors_number(y_p)
#    Y_f = successors_number(y_f)
    
    try:
        
        # create a new model
        m = Model("my_total_milp")
        m.setParam( 'OutputFlag', False )
        
        # create variables x_i
        x = m.addVars(1, length, vtype= GRB.BINARY, name="x")
        
        # create variables zp_i : they're not binary        
        z_p = m.addVars(1, length, vtype= GRB.CONTINUOUS, name="z_p")
            
        # create variables zf_i
        z_f = m.addVars(1, length, vtype= GRB.BINARY, name="z_f")
        
        # objective function FUNCTIONAL + PREFERANCE
#         m.setObjective( sum(alpha * u[i] * z_f[0,i] + (1 - alpha) * u[i] * z_p[0,i] for i in r) , GRB.MAXIMIZE)              
        m.setObjective( sum( u[i] * z_f[0,i] for i in r) , GRB.MAXIMIZE)              
           
        # functional constraints
        m.addConstrs(( z_f[0,i] <= x[0,i] for i in r) , 'cf0')
        
        for i in r:
            if Y_f[i] == 0:
                m.addConstr(( z_f[0,i] <= 1.0 ) , 'cf1' )
            else:
                m.addConstr(( z_f[0,i] <= sum(x[0,j] * y_f[i][j] * pow(Y_f[i],-1) for j in r)), 'cf2' )
        
                      
        # preferance constraints     
        for i in r:
            if Y_p[i] == 0.0:
                m.addConstr( z_p[0,i] <= 1.0 , 'cp1')
            else:
                m.addConstr( (z_p[0,i] <= sum(z_f[0,j] * y_p[i][j] * pow(Y_p[i], -1) for j in r)) , 'cp2' )  
                
        
        m.addConstrs( ( z_p[0,i] <= x[0,i]   for i in r), 'cp3' ) # I can omit this constraint because of z_f <= x
        m.addConstrs( ( z_p[0,i] <= z_f[0,i] for i in r), 'cp4')
        
        # budget constraint
        m.addConstr( ( sum(x[0,i] * c[i] for i in r) <= b ), 'c2' )
        
        m.optimize()        
        
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
        
    list_x = []
    cons = 0
    for i in m.getVars():
        if cons<length:
            list_x.append(i.X)
        cons+=1
    
    print('Milp \n'+ 'Utility: ' + str(m.objVal))
    return m,list_x

    
def printSolution(m):
    if m.status == GRB.Status.OPTIMAL:
        print('\nCost: %g' % m.objVal)
       
    else:
        print('No solution')       
        
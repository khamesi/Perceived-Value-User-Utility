from random_graphs import *
from main_functions import *

n = 10
m = 6
b = 3000


rand_cost = random_energy(n)        
rand_utility = random_utility(n)        
current_max_utility = sum(rand_utility) 

g = new_random_graph(n, m)

# this function create another graph (functional graph) from the graph g
funct_g, pref_g = two_graphs(g)     

# compute the dependencies arrays 
y_p = depend_vector(pref_g)       
y_f = bsf_depend_vector(funct_g, n)    
Y_p = successors_number(y_p)
Y_f = successors_number(y_f) 


"""  ********  MILP  ********  """
# print('milp')
m_milp, milp_sol = complete_milp(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)            
# to get the objective function value (AXIS Y)
obj = m_milp.getObjective()
# y_list_MILP.append(obj.getValue()) 
milp_cost = cost_function(milp_sol, rand_cost)


"""  ******* KNAPSACK  ********  """
# print('knapsack')
knapsack_utility, m_knapsack, knap_sol = knapsack(y_p, y_f, Y_p, Y_f, rand_cost, b, rand_utility, n)
# y_list_KNAPSACK.append(knapsack_utility)
knapsack_cost = cost_function(knap_sol, rand_cost)


"""  ******* REGULAR SIMULATED ANNEALING  ********  """
# print('regular sim ann')
sol = (np.zeros(n))   
SA_solution, SA_u_val, SA_iterations = simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
# y_list_SIM.append(u_val)
# iterations_list_SIM.append(iterations)
SA_cost = cost_function(SA_solution, rand_cost)


# """  ******** MODIFIED SIMULATED ANNEALING ********* """
# print('modified sim ann')

# sol = list(np.zeros(n))     
# SSA_solution, SSA_u_val, SSA_iterations = modified_simulated_annealing(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
# #         y_list_MODSIM.append(u_val)
# #         iterations_list_MODSIM.append(iterations)
# SSA_cost = cost_function(SSA_solution, rand_cost)

"""  ******* GREEDY  ********  """
# print('greedy')
greedy_solution, greedy_utility, greedy_cost, sorted_select_set = greedy_alg(y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
# y_list_GREEDY.append(greedy_utility)


"""  ******* ACYCLIC GREEDY  ********  """
# print('acyclic greedy')
Acyclic_solution, Acyclic_utility, Acyclic_cost= acyclic_greedy_alg(funct_g, y_p, y_f, Y_p, Y_f, sol, rand_cost, rand_utility, b)
# y_list_ACYCLIC_GREEDY.append(Acyclic_utility)



print('Functional Dependency Graph:')
plt.figure(1)
nx.draw(funct_g,with_labels=True)
plt.show()

# print('Preference Dependency Graph:')
# plt.figure(2)
# nx.draw(pref_g,with_labels=True)
# plt.show()



print('Appliance = '+str([int(i) for i in range(n)]))
print('MILP      = '+str([int(i) for i in milp_sol])+' Utility = '+str(m_milp.objVal)+ '  Cost = '+str(milp_cost)+'\n'+
      'KNAPSACK  = '+str([int(i) for i in knap_sol])+' Utility = '+str(knapsack_utility)+ '  Cost = '+str(knapsack_cost)+'\n'+
      'SA        = '+str([int(i) for i in SA_solution])+' Utility = '+str(SA_u_val)+ '  Cost = '+str(SA_cost)+'\n'+
#       'SSA       = '+str([int(i) for i in SSA_solution])+' Utility = '+str(SSA_u_val)+ '  Cost = '+str(SSA_cost)+'\n'+
      'GREEDY    = '+str([int(i) for i in greedy_solution])+' Utility = '+str(greedy_utility)+ '  Cost = '+str(greedy_cost)+'\n'+
      'ACYCLIC   = '+str([int(i) for i in Acyclic_solution])+' Utility = '+str(Acyclic_utility)+ '  Cost = '+str(Acyclic_cost)
     )

# g_f_reduced, Super_nodes = make_acyclic_scc(funct_g)
# print('Condensation Dependency Graph:')
# plt.figure(3)
# nx.draw(g_f_reduced,with_labels=True)
# plt.show()

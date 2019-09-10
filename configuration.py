# -*- coding: utf-8 -*-
"""
Configuration file
All global variable used to analize the data in different ways

@author: dolcev
"""
import numpy as np
from collections import OrderedDict

time_slot = 15  # minute to do the AND 
n_hours = 6
total_rows = int(24/n_hours)
n_minutes = int(60/time_slot)


output_folder = 'Average_Value\\'
#folder_list = ['Alarmclock', 'Coffeemaker', 'Dishwasher', 'MicrowaveOven', 'Toaster', 'Washingmachine']

folder_list = ['TV-LCD']
#threshold_list = [5, 5, 5, 4, 5, 5]  #[5,5,2]

# max wattage for each device. it's a ordered dictionary, so it returns the values in the same order
energy_dic = OrderedDict([('Alarmclock',35) ,('Coffeemaker',1500), ('Dishwasher',3000),('MicrowaveOven',1500) ,('Toaster',800), ('Washingmachine',2500)])
energy_array = np.array(list(energy_dic.values()))
#wattage_list = [35, 1500, 3000, 1500, 800, 2500]
# array of cost values
#cost_array = np.array(wattage_list)


# values of utility for each device
#dev_utility = {'Alarmclock': 41, 'Coffeemaker': 50, 'Dishwasher':41, 'MicrowaveOven':8, 'Toaster':33, 'Washingmachine':16}
utility_dic = OrderedDict([('Alarmclock',41) ,('Coffeemaker',50), ('Dishwasher',41),('MicrowaveOven',8) ,('Toaster',33), ('Washingmachine',16)])
utility_array = np.array(list(utility_dic.values()))

# budget limit
#budget= 7000 # more than half sum of wattage_list

# limited depth for BFS
# search_depth = n

# alpha value used in MILP problem (gurobi)
alpha = 1






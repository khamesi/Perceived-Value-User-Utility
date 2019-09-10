# -*- coding: utf-8 -*-
"""
Calculate the usage probability for each hour, using the binary array

@author: dolcev
"""

import pandas as pd
import numpy as np
from logical_and import logical_and
from logical_and import list_and
from configuration import *


def absolute_prob(my_list, prob, output_col):
    
    # prob is the DataFrame where the function stores the values
    out = []
    for h in range(total_rows):
        # df[0-59], df[60-119] ..
        start = h * (n_minutes*n_hours)
        end = (h+ 1) * (n_minutes*n_hours) 
        sub_array = my_list[ start : end ]
        
        #tot_true = sum(my_list)
        out.append(sum(sub_array) / (n_minutes*n_hours))
#        if tot_true != 0:
#            out.append(sum(sub_array) / tot_true)
#        else:
#            out.append(0)
    prob[output_col] = out


def joint_prob(dic, folder_list, output_folder, out_joint_prob):
    
    """
    JOINT PROBABILITIES FOR COUPLES OF DEVICES
    
    PART 1 : calculate the logical AND between each couple of devices (no repetitive)
             for each minute
    """
    # empty list for couples of devices
    l = []
    
    # create a list with the name of columns for the joint_prob
    # ex. Alarmclock_&_Coffeemaker, Alarmclock_&_Dishwasher
    for i in range(len(folder_list)-1):
        j=i
        for j in range(i + 1, len(folder_list)):       
            l.append(folder_list[i]+ '_&_' + folder_list[j])
        
    # create a new Dictionary for the AND boolean values for each no-repetitive couple of devices
    # ex. A and B , A and C, B and C 
    # I get a boolean value if both A and B are True in the same slot time   
    dic_and = {}
    
    list_and(dic, folder_list, dic_and)
    
    """
    JOINT PROBABILITIES FOR COUPLES OF DEVICES
    
    PART 2 : calculate the joint probability for each couple of devices 
             using the same function to calculate the absolute probability
             It's just a statistic approach (number_value_true/60)
    """
   
    for i in range(len(l)) :
        absolute_prob(dic_and[l[i]], out_joint_prob, l[i])

        
def cond_prob(folder_list, abs_prob, j_prob, dic):
    
    for i in folder_list:
        for j in folder_list:
            if i == j:
                continue
            else:
                index_a = folder_list.index(i)
                index_b = folder_list.index(j)
            
#                # numerator p(A and B)  [convert series to list]
#                if index_a < index_b:                
#                    num = j_prob[i + '_&_' + j].tolist()  
#                else:
#                    num = j_prob[j + '_&_' + i].tolist()
                
                # numerator p(A and B)  [convert series to list]
                if index_a < index_b:                
                    num = j_prob[i + '_&_' + j]
                else:
                    num = j_prob[j + '_&_' + i]
                
                # denominator p(B) [convert series to list]
                den = abs_prob[j]
    
                # empty list to calculate the division
                out = []
                # division between 2 list num and den
                for r in range(len(den)):
                    if den[r] == 0 :    # to avoid division for zero
                        out.append(0)
                    else:
                        out.append(num[r]/den[r])
                        
                #out = [num / den for num, den in zip(num, den)]
                       
                dic['condit_prob_'+ i][j] = out
                
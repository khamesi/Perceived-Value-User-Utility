# -*- coding: utf-8 -*-
"""
Thresholding average array using a different threshold for each device
furthermore save the binary array in a csv file and even the plot like png image

@author: dolcev
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from scipy.stats import threshold

from configuration import *


def thresholding(output_folder, current_device, t):
    
    path = output_folder + current_device+'_avg\\'+ current_device+'_weekly_avg.csv'
    # import the dishwasher weekly average
    df = pd.read_csv(path, sep = ';', header = None)
    
    # select just the wattage value and convert to array
    array = df[1][:]
    array = np.array(array)
   
    #out = threshold(a, t) # 2 is the threshold
    
    # thresholding to get a binary file
    bin_val = array >= t
    
    out = []

    if time_slot == 1:
        out = bin_val

    else:
        my_range = int(len(bin_val)/time_slot )
        
        # try if the bin values are more the a half of minutes in one time slot
        for i in range(my_range):
            start = i * time_slot
            end =((i + 1) * time_slot) 
            
            if any( bin_val[ start : end ] ) == True:
            #if sum( bin_val[start : end ]) >= (60/ (2 * time_slot)) :
                out.append(True)
            else:
                out.append(False)
    
    #destination_folder = output_folder+current_device+'_avg\\'
    # save the binary Dataframe like csv file
    #df.to_csv(destination_folder+current_device+'_bin_average.csv', sep=';', float_format='%.3f', header= False, index=False)
    #save_plot(df, current_device + 'Binary Weekly Average', 1, 2, destination_folder+current_device+'_bin_average')
      
    return out



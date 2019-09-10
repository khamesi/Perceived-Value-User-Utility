# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 14:20:39 2017

@author: dolcev
"""
import pandas as pd

def logical_and(folder_list, output_folder, out_df):
    
    index = 1
    
    for i in range(len(folder_list)-1):
        j=i
        for j in range(i + 1, len(folder_list)):       
            file_path1 = output_folder+folder_list[i]+'_avg\\'+ folder_list[i]+'_bin_average.csv'
            file_path2 = output_folder+folder_list[j]+'_avg\\'+ folder_list[j]+'_bin_average.csv'
            
            df1 = pd.read_csv(file_path1, sep = ';', header = None)
            df2 = pd.read_csv(file_path2, sep = ';', header = None)
            
            index_and = folder_list[i]+ '_&_' + folder_list[j]
            
            #calculate the probability of the intersection of A and B
            # convert series to list
            list1 = df1[index].tolist()
            list2 = df2[index].tolist()
            
            # Logic AND between 2 boolean lists
            out = [list1 and list2 for list1, list2 in zip(list1, list2)]
            out_df[index_and] = out

#            temp_list = []
#            for k in range(int(len(list1)/slot)):
#                sub1 = list1[0 + k * slot : (slot - 1) + k * slot]
#                sub2 = list2[0 + k * slot : (slot - 1) + k * slot]
#                if any(sub1)==True and any(sub2)==True:
#                    temp_list.extend([True] * slot)
#                else:
#                    temp_list.extend([False] * slot)
#            
#            out_df[index_and] = temp_list                      
    
    return out_df
    
    
def list_and(dic, folder_list, out_df):
    
    for i in range(len(folder_list)-1):
        j=i
        for j in range(i + 1, len(folder_list)):       
            
            list1 = dic[folder_list[i]]
            list2 = dic[folder_list[j]]
            
            index_and = folder_list[i]+ '_&_' + folder_list[j]
            
            # Logic AND between 2 boolean lists
            out = [list1 and list2 for list1, list2 in zip(list1, list2)]
            out_df[index_and] = out
    


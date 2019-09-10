# -*- coding: utf-8 -*-
"""
Create a plot and save it like png image
X axis -> Time (hours)
Y axis -> Watt

@author: dolcev
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def save_plot(df, title, index1, index2, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Watt')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # set the date format  on X axis
    ax.plot_date(df[index1] ,df[index2],fmt='-', xdate=True, ydate=False)
    fig.savefig(file_name + '.png', dpi=150)
    
    return True

    
def xy_plot(x, y, title, xlabel, ylabel, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y)
    #fig.savefig(file_name + '.png', dpi=100)
    
    return True   
    
def xy_plot2(x, y1, y2, title, xlabel, ylabel, ylabel_1, ylabel_2, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, '--bo', label = ylabel_1 )
    ax.plot(x, y2, '--r*', label = ylabel_2 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='upper right', shadow = False, fontsize='x-large')
    #fig.savefig(file_name + '.png', dpi=100)
    
    return True 

def xy_plot4(x, y1, y2, y3, y4, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
#     ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, '-ro' , label = ylabel_1)
    ax.plot(x, y2, '-b+', label = ylabel_2 )
    ax.plot(x, y3, '-yx' , label = ylabel_3)
    ax.plot(x, y4,'-g>' , label = ylabel_4 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='upper left', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True

def xy_plot4_right(x, y1, y2, y3, y4, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
#     ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, '-ro' , label = ylabel_1)
    ax.plot(x, y2, '-b+', label = ylabel_2 )
    ax.plot(x, y3, '-yx' , label = ylabel_3)
    ax.plot(x, y4, '-g>' , label = ylabel_4 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='upper right', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True 

def xy_plot4_left_down(x, y1, y2, y3, y4, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
#     ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, '-ro' , label = ylabel_1)
    ax.plot(x, y2, '-b+', label = ylabel_2 )
    ax.plot(x, y3, '-yx' , label = ylabel_3)
    ax.plot(x, y4,'-g>' , label = ylabel_4 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='lower left', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True

def xy_plot4_right_down(x, y1, y2, y3, y4, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
#     ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, '-ro' , label = ylabel_1)
    ax.plot(x, y2, '-b+', label = ylabel_2 )
    ax.plot(x, y3, '-yx' , label = ylabel_3)
    ax.plot(x, y4, '-g>' , label = ylabel_4 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='lower right', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True 


def xy_plot5(x, y1, y2, y3, y4, y5, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, ylabel_5, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, label = ylabel_1 )
    ax.plot(x, y2, label = ylabel_2 )
    ax.plot(x, y3, label = ylabel_3 )
    ax.plot(x, y4, label = ylabel_4 )
    ax.plot(x, y5, label = ylabel_5 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='upper left', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True

def xy_plot5_right(x, y1, y2, y3, y4, y5, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, ylabel_5, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, label = ylabel_1 )
    ax.plot(x, y2, label = ylabel_2 )
    ax.plot(x, y3, label = ylabel_3 )
    ax.plot(x, y4, label = ylabel_4 )
    ax.plot(x, y5, label = ylabel_5 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='upper right', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True 


def xy_plot6(x, y1, y2, y3, y4, y5, y6, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, ylabel_5, ylabel_6, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, label = ylabel_1 )
    ax.plot(x, y2, label = ylabel_2 )
    ax.plot(x, y3, label = ylabel_3 )
    ax.plot(x, y4, label = ylabel_4 )
    ax.plot(x, y5, label = ylabel_5 )
    ax.plot(x, y6, label = ylabel_6 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='upper left', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True 

def xy_plot6_right(x, y1, y2, y3, y4, y5, y6, title, xlabel, ylabel, ylabel_1, ylabel_2, ylabel_3, ylabel_4, ylabel_5, ylabel_6, file_name):
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_title('\n'+title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(x, y1, label = ylabel_1 )
    ax.plot(x, y2, label = ylabel_2 )
    ax.plot(x, y3, label = ylabel_3 )
    ax.plot(x, y4, label = ylabel_4 )
    ax.plot(x, y5, label = ylabel_5 )
    ax.plot(x, y6, label = ylabel_6 )
    #ax.set_ylim(0, 105)
    ax.legend(loc='upper right', shadow = False, fontsize='x-large')
    plt.grid(b=None, which='major', axis='both',color='k', linestyle='-', linewidth=.2)
    fig.savefig(file_name + '.png', dpi=100)
    fig.savefig(file_name + '.eps', dpi=100)
    
    return True 

#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
#from openpyxl import load_workbook

data = open('bostonProperty.csv','r')
lines = data.readlines()
data.close()

value,area,year,view,ac = ([],[],[],[],[])

for i in range(1,len(lines)):
    row = lines[i].strip().split(',')
    
    if row[11-1] in ('R1','R2','R3','R4'):#K

        #outlier
        if int(row[26-1]) > 10000:
            continue
        
        value.append(int(row[20-1]))#T
        area.append(int(row[26-1]))#Z
        year.append(int(row[23-1]))#W
        view.append(row[50-1])#R_VIEW = AX
        
        ac_type = row[44-1]
        color = 'gray'
        if ac_type in ('C','D'):
            color = 'red'
            pass
        ac.append(color)#R_AC = AR
        
        pass

    pass

n = len(value)

#categorical
#scatter plot: assessed value against total living area
#Blue-Black-Red color indicates A/C type

def valueVsArea(plt):
    
    #move the red points to the end (draw on top)
    back = n-1
    for i in range(n):
        if i!=back and ac[i] == 'red':
            area[i], area[back] = (area[back],area[i])
            value[i], value[back] = (value[back],value[i])
            ac[i], ac[back] = (ac[back],ac[i])
            back -= 1
            pass
        pass
    
    ## labels, title, legend
    
    plt.scatter(area, value, c=ac,marker='.')
    plt.xlabel("Total living area (square feet)")
    plt.ylabel("Total property value")
    #plt.legend(loc=2)
    
    ## display and save
    plt.show()
    #plt.savefig('value-vs-area.png')
    pass

#valueVsArea(plt)

#continuous
#stacked bar plot: one bar per ac type, height for number of parcels
#each stack is age range (i.e. decade built)


#diverging
#determine min,median,max values; map to blue,purple,red
#segment values into five bins
#stacked bar plot: for each view quality, total bar height is no. of buildings


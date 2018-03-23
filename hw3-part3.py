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
        try:
            value.append(int(row[20-1]))#T
            area.append(int(row[26-1]))#Z
            year.append(int(row[23-1]))#W
            view.append(row[50-1])#R_VIEW = AX
            ac.append(row[44-1])#R_AC = AR
            pass
        except:
            print row
            print len(row)
            break
        pass
    pass


#scatter plot: assessed value against total living area
#each point is a black circle
#fill white for oldest
#fill black for newest
#for intermediary values, interpolate luminance between
def linePlot(plt):
    
    #plt.gcf().autofmt_xdate()

    ## labels, title, legend
    plt.scatter(area, value, c="g")
    plt.xlabel("Total living area (square feet)")
    plt.ylabel("Total property value")
    #plt.legend(loc=2)
    
    ## display and save
    plt.show()
    #plt.savefig('value-vs-area.png')
    pass


#bar chart: number of buildings with each A/C type
#Blue-Black-Red color indicates A/C type


#find the q-tiles of the assessed values
#map each q-tile to a color on the red-blue gradient
#stacked bar plot: bar height is number of buildings with each view quality
#blue-red color gradient encodes distribution of assessed value

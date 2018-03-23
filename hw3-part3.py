#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from math import floor

data = open('bostonProperty.csv','r')
lines = data.readlines()
data.close()

value,area,year,cond,ac = ([],[],[],[],[])
condToIndex = {'A':0,'E':1,'F':2,'G':3,'P':4,'S':5}
conditionToIndex = {'A':0,'E':1,'F':2,'G':3,'P':4}

for i in range(1,len(lines)):
    row = lines[i].strip().split(',')
    
    if row[11-1] in ('R1','R2','R3','R4'):#K

        #outlier area (one point)
        if int(row[26-1]) > 10000: continue

        #outlier value (two points)
        if int(row[20-1]) > 1000000: continue
        
        #houses can't be that old
        if int(row[23-1]) < 1492: continue

        #we want rows with view data
        #if row[50-1] not in viewToIndex.keys(): continue
        if row[47-1] not in conditionToIndex.keys(): continue
        
        value.append(int(row[20-1]))#T
        area.append(int(row[26-1]))#Z
        year.append(int(row[23-1]))#W
        cond.append(row[47-1])#R_OVERALL_COND = AU
        
        ac_type = row[44-1]
        color = 'gray'
        if ac_type in ('C','D'):
            color = 'red'
            pass
        ac.append(color)#R_AC = AR
        
        pass

    pass

n = len(value)

#Tasks: are houses with ac common? if two houses have the same area, does having ac increase the value?
#encoding: scatter plot
#color map: categorical, with red indicating having ac and gray for not

def valueVsArea(plt):
    
    #move the red points to the end (draw on top)
    back = n-1
    for i in range(n):
        
        if i!=back and ac[i] == 'red':
            area[i], area[back] = (area[back],area[i])
            value[i], value[back] = (value[back],value[i])
            ac[i], ac[back] = (ac[back],ac[i])
            year[i], year[back] = (year[back],ac[i])
            cond[i], cond[back] = (cond[back],ac[i])

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


#Task: what is the distribution of house age and size?
#encoding: heatmap
#continuous color map (white-black)

def ageVsArea(plt):
    la,ua,ly,uy = min(area),max(area),min(year),max(year)
    #every 500 sq ft gets a bin
    abins = 1 + ((ua-la) / 500)
    #every decade gets a bin
    ybins = 1 + ((uy-ly) / 10)
    
    heatmap = []
    for i in range(abins):
        heatmap.append([])
        for j in range(ybins):
            heatmap[-1].append(0)
            pass
        pass

    for i in range(n):
        y = year[i]
        a = area[i]
        heatmap[(a-la)/500][(y-ly)/10] += 1
        pass
    
    plt.imshow(heatmap, cmap='gray_r', extent=[ly,uy,ua,la],
               interpolation='nearest',aspect='auto')
    
    plt.show()
    pass

ageVsArea(plt)

##Task: what is the distribution of value for each building style?
##encoding: stacked bar plot (a heatmap isn't as pleasing)
##color map: diverging
##  determine min,median,max values; map to blue,purple,red
##  segment values into six bins

def valueVsCondition(plt):
    numStacks = 10
    
    sv = sorted(value)
    lv,mv,uv = sv[0],sv[n/2],sv[n-1]
    lowerBinSize = (mv-lv)/(numStacks/2)
    upperBinSize = (uv-mv)/(numStacks/2)
    
    bars = []
    for i in range(numStacks):
        bars.append([])
        ## 5 bars, one for each condition
        for j in range(5):
            bars[-1].append(0)
            pass
        pass
    
    #print lv,mv,uv
    for i in range(n):
        v = value[i]
        
        condBar = conditionToIndex[cond[i]]

        ##bottom half
        if v <= mv:
            bars[min(numStacks/2 - 1,(v-lv)/lowerBinSize)][condBar] += 1
            pass
        ##top half
        else:
            bars[min(numStacks-1,numStacks/2+(v-mv)/upperBinSize)][condBar] += 1
            pass
        
        pass
    print bars
    
    width = 0.35
    ind = np.arange(5)
    bottom = [0,0,0,0,0]
    cmap = plt.get_cmap('coolwarm')
    
    for i in range(numStacks):
        plt.bar(ind,bars[i],width,bottom=bottom,color=cmap(i/float(numStacks)))
        for j in range(5):
            bottom[j] += bars[i][j]
            pass        
        pass
    
    plt.show()
    pass

valueVsCondition(plt)

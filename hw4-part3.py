#!/usr/bin/python

from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
from math import floor

data = open('bostonProperty.csv','r')
lines = data.readlines()
data.close()

##columns of interest
value,area,year,cond,ac = ([],[],[],[],[])

##converts the string to an integer
conditionToIndex = {'A':0,'E':1,'F':2,'G':3,'P':4}

##I am interested in residential buildings only
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
        
        ac_type = row[44-1]#R_AC = AR

        hasAC = True
        if ac_type == 'N': #alternatives: ('C','D'):
            hasAC = False
            pass
        ac.append(hasAC)
        
        pass

    pass

n = len(value)

#Tasks: any correlation between area and value? if two houses have the same area, does having ac increase the value?
#encoding: scatter plot
#color map: categorical, with red indicating having ac and gray for not

def valueVsArea(plt):

    ##partition by ac
    areaFalse,areaTrue,valueFalse,valueTrue = [],[],[],[]
    for i in range(n):
        if ac[i]:
            areaTrue.append(area[i])
            valueTrue.append(value[i])
            pass
        else:
            areaFalse.append(area[i])
            valueFalse.append(value[i])
            pass
        pass
    
    ## actually plot the data
    plt.scatter(areaFalse, valueFalse, c='gray',marker='.',label='No A/C')
    plt.scatter(areaTrue, valueTrue, c='red',marker='.',label='A/C')

    ## labels, title, legend    
    plt.xlabel("Total living area (square feet)")
    plt.ylabel("Total property value")
    plt.legend(loc=4)
    plt.title('Residential Building Value vs Area')

    ## display and save
    plt.show()
    #plt.savefig('value-vs-area.png')
    pass

valueVsArea(plt)


#Task: what is the distribution of house age and size?
#encoding: heatmap
#continuous color map (white-black)

def ageVsArea(plt):
    la,ua,ly,uy = min(area),max(area),min(year),max(year)
    #every 100 sq ft gets a bin
    abins = 1 + ((ua-la) / 100)
    #every decade gets a bin
    ybins = 1 + ((uy-ly) / 10)

    ## make bins
    heatmap = []
    for i in range(abins):
        heatmap.append([])
        for j in range(ybins):
            heatmap[-1].append(0)
            pass
        pass

    ## fill bins
    for i in range(n):
        y = year[i]
        a = area[i]
        heatmap[(a-la)/100][(y-ly)/10] += 1
        pass

    ## make the heatmap
    plt.imshow(heatmap, cmap='gray_r', extent=[ly,uy,ua,la],
               interpolation='nearest',aspect='auto')
    plt.title('Distribution of Residential Buildings, by Area & Age')
    plt.ylabel('Living Area, in 100 sq ft')
    plt.xlabel('Year Built')

    plt.colorbar(label='Number of buildings')
    
    plt.show()
    pass

ageVsArea(plt)

##  Tasks: how many houses are of excellent/average/poor quality? what is the distribution of value for each category?
##  encoding: stacked bar plot (a heatmap isn't as pleasing)
##  color map: diverging
##    determine min,median,max values; map to blue,purple,red
##    segment this domain into bins such that the middle bin(s) are at the median

def valueVsCondition(plt):
    numStacks = 12

    ## find min, median, max
    sv = sorted(value)
    lv,mv,uv = sv[0],sv[n/2],sv[n-1]
    binSize = (uv - lv) / float(numStacks)
    lowerBinSize = (mv-lv)/(numStacks/2)
    upperBinSize = (uv-mv)/(numStacks/2)

    ## define bins = stacks in the bar chart
    bars = []
    for i in range(numStacks):
        bars.append([])
        ## 5 bars, one for each condition
        for j in range(5):
            bars[-1].append(0)
            pass
        pass

    ## fill the bins = determine size of each stack
    
    for i in range(n):
        v = value[i]

        condBar = conditionToIndex[cond[i]]
        bars[min(int((v-lv)/binSize),numStacks-1)][condBar] += 1

        pass

    ## bin containing median value should be gray
    medBin = int((mv-lv) / binSize)
    
    ## plot the data
    width = 0.35
    ind = np.arange(5)
    ## the bottom of each layer of bars varies
    bottom = [0,0,0,0,0]
    cmap = plt.get_cmap('coolwarm')    

    for i in range(numStacks):
        begin,end = lv+i*binSize,lv+(i+1)*binSize
        if i < numStacks-1: end -= 1

        if i <= medBin: color = (float(i)/medBin) / 2.0
        else: color = 0.5 + (float(i)-medBin)/(2*(numStacks-medBin))
        
        plt.bar(ind,bars[i],width,bottom=bottom,
                color=cmap(color),
                label='%d - %d'% (begin,end))
        for j in range(5):
            bottom[j] += bars[i][j]
            pass
        pass

    ## title, axes, legend
    plt.title('Residential Building Value across Quality')
    plt.ylabel('Number of buildings')
    plt.xlabel('Overall building condition')
    plt.xticks(ind,['Average','Excellent','Fair','Good','Poor'])
    plt.legend(loc=1,title='Value Bracket')

    plt.show()
    pass

valueVsCondition(plt)

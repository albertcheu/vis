#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

#Date plotting obtained from https://stackoverflow.com/a/9627970
import matplotlib.dates as dates
import datetime as dt

from horizon import horizon
#from splom import splom

## loop through the csv's
filenames = ['DowJones','NASDAQ','NYSE','SP500']
suffix = '-HistoricalPrices.csv'

values = []
changes = []
days = []
for fname in filenames:

    values.append([])
    changes.append([])
    days.append([])
    
    data = open(fname+suffix)
    lines = data.readlines()[1:]
    data.close()

    ##reverse the list to be in chronological order
    lines.reverse()
    initValue = 0
    for line in lines:

        ## record the date
        row = line.split(',')
        days[-1].append(dt.datetime.strptime(row[0],'%m/%d/%y').date())

        ##record value
        value = float(row[-1])
        values[-1].append(value)
        
        ## record percent changed
        if initValue == 0:        
            initValue = value
            pass
        changes[-1].append((value - initValue) / initValue)

        pass
    pass


## Figure 1: Small-multiple line charts
def fig1(plt,days,values):
    fig, axes = plt.subplots(2,2,figsize=(8,4))

    ## plot each index
    for i in range(4):
        
        ## display MM/DD/YYYY
        axes[i/2,i%2].xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%y'))
    
        ## label each new day/month/year
        axes[i/2,i%2].xaxis.set_major_locator(dates.MonthLocator())
        
        ## plot the i-th time series
        axes[i/2,i%2].plot(days[i],values[i])
        axes[i/2,i%2].grid()

        ## title and ylabel
        axes[i/2,i%2].set(title=filenames[i])
        if i%2 == 0: axes[i/2,i%2].set(ylabel='Value')
        if i > 1: axes[i/2,i%2].set(xlabel='Time')
        pass

    plt.gcf().autofmt_xdate()
    
    ## display and save
    #plt.show()
    plt.savefig('stockMarket-SmallMultLine.png')
    
    pass

fig1(plt,days,values)

#### Figure 2: Horizon graphs
def fig2(plt,days,values):

    fig, axes = plt.subplots(4,1,figsize=(8,4))
    plt.subplots_adjust(hspace=0.5)

    ## plot each index
    for i in range(4):
    
        ## display MM/DD/YYYY
        axes[i].xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%y'))
    
        ## label each new day/month/year
        axes[i].xaxis.set_major_locator(dates.MonthLocator())
        
        ## break up the i-th time series into quartiles
        horizon(axes[i],days[i],values[i],4)
        
        axes[i].grid()
        axes[i].set(title=filenames[i],ylabel='Value',xlabel='Time')
        
        pass

    plt.gcf().autofmt_xdate()
    
    ## display and save
    #plt.show()
    plt.savefig('stockMarket-Horizon.png')
    pass

fig2(plt,days,values)

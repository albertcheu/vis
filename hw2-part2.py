#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

#Date plotting modified from https://stackoverflow.com/a/9627970
import matplotlib.dates as dates
import datetime as dt

from splom import splom
from horizon import horizon

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

def linePlot(plt):
    fig, ax = plt.subplots()

    ## display MM/DD/YYYY
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
    
    ## label each new day/month/year
    plt.gca().xaxis.set_major_locator(dates.MonthLocator())
    
    ## plot each index    
    for i in range(4):
        ## pair the i-th time series with its name
        ax.plot(days[i],changes[i],label=filenames[i])
        pass
    
    plt.gcf().autofmt_xdate()

    #labels, title, legend
    ax.set(xlabel='Time',ylabel='Fractional change',
           title='Stock Market Indices from 2017 to 2018')
    ax.grid()
    ax.legend()

    ## display and save
    ##plt.show()
    plt.savefig('stockMarket-Line.png')
    pass

##linePlot(plt)

def barPlot(plt):
    ## number of days to display, width of bar, and list from 0 to numdays-1
    numdays = 30
    width =0.23
    ind = np.arange(numdays)

    ## Plot the data (make wide enough to see tick labels)
    fig, ax = plt.subplots(1,1,figsize=(8,4))
    for i in range(4):
        ax.bar(ind + i*width, changes[i][:numdays], width, label=filenames[i])
        pass
    
    ## Labels, title, and legend
    ax.set_xticks(ind)
    ax.set(xlabel='Business Days since 2 Feb',
           ylabel='Fractional change',
           title='Stock Market Indices from 3 Feb to 17 March, 2017')
    ax.grid()
    ax.legend()

    ## display and save
    ##plt.show()
    plt.savefig('stockMarket-Bar.png')
    
    pass

#barPlot(plt)


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

#fig1(plt,days,values)

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

#fig2(plt,days,values)

#### Figure 3: Scatter-plot matrix
def fig3(plt,values):

    splom(plt,values,filenames,'Correlations between market indices, Feb 2017 - Feb 2018')
    #plt.show()
    plt.savefig('stockMarket-SPLOM.png')
    pass

#fig3(plt,values)

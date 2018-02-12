#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

#Date plotting modified from https://stackoverflow.com/a/9627970
import matplotlib.dates as dates
import datetime as dt

## loop through the csv's
filenames = ['DowJones','NASDAQ','NYSE','SP500']
suffix = '-HistoricalPrices.csv'
changes = []
days = []
for fname in filenames:
    
    changes.append([])
    days.append([])
    
    data = open(fname+suffix)
    lines = data.readlines()[1:]
    data.close()

    numdays = len(lines)
    
    ##reverse the list to be in chronological order
    lines.reverse()
    initScore = 0
    for line in lines[:numdays]:

        ## record the date
        row = line.split(',')
        days[-1].append(dt.datetime.strptime(row[0],'%m/%d/%y').date())

        ## record percent changed
        score = float(row[-1])
        if initScore == 0:        
            initScore = score
            pass
        changes[-1].append((score-initScore) / initScore)
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

barPlot(plt)

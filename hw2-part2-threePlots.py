#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

#Date plotting obtained from https://stackoverflow.com/a/9627970
import matplotlib.dates as dates
import datetime as dt

from splom import splom as splom

## loop through the csv's
filenames = ['DowJones','NASDAQ','NYSE','SP500']
suffix = '-HistoricalPrices.csv'

scores = []
changes = []
days = []
for fname in filenames:

    scores.append([])
    changes.append([])
    days.append([])
    
    data = open(fname+suffix)
    lines = data.readlines()[1:]
    data.close()

    ##reverse the list to be in chronological order
    lines.reverse()
    initScore = 0
    for line in lines:

        ## record the date
        row = line.split(',')
        days[-1].append(dt.datetime.strptime(row[0],'%m/%d/%y').date())

        ##record score
        score = float(row[-1])
        scores[-1].append(score)
        
        ## record percent changed
        if initScore == 0:        
            initScore = score
            pass
        changes[-1].append((score - initScore) / initScore)

        pass
    pass


## Figure 1: Small-multiple line charts
fig, axes = plt.subplots(2,2)

## plot each index
for i in range(4):
    
    ## display MM/DD/YYYY
    axes[i/2,i%2].xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%y'))
    
    ## label each new day/month/year
    axes[i/2,i%2].xaxis.set_major_locator(dates.MonthLocator())
    
    ## pair the i-th time series with its name
    axes[i/2,i%2].plot(days[i],changes[i])
    axes[i/2,i%2].grid()
    ##axes[i/2,i%2].legend()
    axes[i/2,i%2].set(title=filenames[i])
    if i%2 == 0: axes[i/2,i%2].set(ylabel='Value')
    pass

plt.gcf().autofmt_xdate()
#ax.set(xlabel='Time',
#       ylabel='Value',
#       title='Stock Market Indices from 2017 to 2018')


splom()

## display and save
#plt.show()
#plt.savefig('stockMarket-Line.png')

fig = splom()

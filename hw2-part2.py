#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

#Date plotting obtained from https://stackoverflow.com/a/9627970
import matplotlib.dates as dates
import datetime as dt

numdays = 30

fig, ax = plt.subplots()

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

## display MM/DD/YYYY
plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))

## label each new day/month/year
plt.gca().xaxis.set_major_locator(dates.MonthLocator())

## plot each index
width =0.23
ind = np.arange(numdays)
for i in range(4):
    ## pair the i-th time series with its name

    ## Swap for line plot
    ax.plot(days[i],changes[i],label=filenames[i])
    #ax.bar(ind + i*width, changes[i], width, label=filenames[i])
    
    pass

plt.gcf().autofmt_xdate()
#ax.set_xticks(ind)
ax.set(#xlabel='Business Days since 2 Feb',
       xlabel='Time',
       ylabel='Fractional change',
       ## Swap for line plot
       title='Stock Market Indices from 2017 to 2018')
       #title='Stock Market Indices from 3 Feb to 17 March, 2017')

ax.grid()
ax.legend()

## display and save
#plt.show()
plt.savefig('stockMarket-Line.png')
#plt.savefig('stockMarket-Bar.png')

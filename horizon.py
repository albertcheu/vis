def horizonHelper(ax,x,y,numLayers,color):
    zeroes = list(0 for xval in x)
    
    ## find how much vertical space each layer will take
    ymin,ymax = min(y),max(y)
    step = (ymax-ymin) / numLayers

    ## each layer is a different plot
    for i in range(numLayers):
        yi = []
        for yval in y:
            if yval >= ymin+i*step and yval <= ymin+(i+1)*step:
                yi.append(yval - (ymin+i*step))
                pass
            elif yval < ymin+i*step: yi.append(0)
            else: yi.append(step)
            pass
        #ax.plot(x,yi,color=color,alpha=float((i+1))/numLayers)
        ax.fill_between(x,yi,zeroes,color=color,alpha=float(i+1)/numLayers)
        pass
    
    pass

def horizon(ax,x,y,numLayers):
    ##positives
    pos = []
    for yval in y:        
        if yval >= 0: pos.append(yval)
        else: pos.append(0)
        pass
    horizonHelper(ax,x,pos,numLayers,'blue')
    
    ##negatives
    neg = []
    for yval in y:
        if yval < 0: neg.append(-yval)
        else: neg.append(0)
        pass
    horizonHelper(ax,x,neg,numLayers,'red')

    pass

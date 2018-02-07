def horizonHelper(ax,x,y,numLayers,color):

    
    ## find how much vertical space each layer will take
    ymin,ymax = min(y),max(y)
    step = (ymax-ymin) / numLayers

    ## each layer is a different plot
    for i in range(numLayers):
        xi,yi = [],[]
        for j in range(len(x)):
            xval,yval = x[j],y[j]
            
            if yval >= ymin+i*step and yval <= ymin+(i+1)*step:
                xi.append(xval)
                yi.append(yval - (ymin+i*step))
                pass
            
            elif yval > ymin+(i+1)*step:
                xi.append(xval)
                yi.append(step)
                pass
            
            #elif yval < ymin+i*step: yi.append(0)
            #else: yi.append(step)
            
            pass
        
        zeroes = list(0 for yval in yi)
        ax.fill_between(xi,yi,zeroes,color=color,
                        alpha=(float(i+1)/numLayers)**2)
        pass
    
    pass

def horizon(ax,x,y,numLayers):
    xpos,ypos = [],[]
    xneg,yneg = [],[]
    for j in range(len(x)):
        xval,yval = x[j],y[j]

        if yval >= 0:
            ypos.append(yval)
            xpos.append(xval)
            pass
        else:
            yneg.append(-yval)
            xneg.append(xval)
            pass
        pass
    if len(ypos): horizonHelper(ax,xpos,ypos,numLayers,'blue')
    if len(yneg): horizonHelper(ax,xneg,yneg,numLayers,'red')
    
    # ##positives
    # pos = []
    # for yval in y:        
    #     if yval >= 0: pos.append(yval)
    #     else: pos.append(0)
    #     pass
    # horizonHelper(ax,x,pos,numLayers,'blue')
    
    # ##negatives
    # neg = []
    # for yval in y:
    #     if yval < 0: neg.append(-yval)
    #     else: neg.append(0)
    #     pass
    # horizonHelper(ax,x,neg,numLayers,'red')

    pass

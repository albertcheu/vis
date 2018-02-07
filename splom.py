#### *Heavy* modification of code from https://stackoverflow.com/a/7941594

def splom(plt, data, names, title=None):
    """
    Plots a scatterplot matrix of subplots.
    Each row of "data" is plotted against other rows, resulting in a nrows by nrows grid of subplots with the diagonal subplots labeled with "names".
    Additional keyword arguments are passed on to matplotlib's "plot" command.
    Returns the matplotlib figure object containg the subplot grid.
    """
    
    nfeatures = len(data)
    fig, axes = plt.subplots(nrows=nfeatures, ncols=nfeatures, figsize=(8,8))
    fig.subplots_adjust(hspace=0.05, wspace=0.05)

    ## Display settings
    for ax in axes.flat:
        ## Hide all ticks and labels by default
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        ## Set up ticks only on one side for "outer" subplots
        if ax.is_first_col():
            ax.yaxis.set_ticks_position('left')
            ax.yaxis.set_visible(True)
        if ax.is_last_col():
            ax.yaxis.set_ticks_position('right')
            ax.yaxis.set_visible(True)
        if ax.is_first_row():
            ax.xaxis.set_ticks_position('top')
            ax.xaxis.set_visible(True)
        if ax.is_last_row():
            ax.xaxis.set_ticks_position('bottom')
            ax.xaxis.set_visible(True)
        pass

    ## Actually plot the data
    for i in range(nfeatures):
        for j in range(nfeatures):
            if i == j:
                axes[i,j].xaxis.set_visible(False)
                axes[i,j].yaxis.set_visible(False)
                continue
            
            axes[i,j].plot(data[j],data[i],
                            linestyle='none',
                            marker='.', color='black',
                            mfc='none'
            )
            
            pass
        pass
    
    # Label the diagonal subplots
    for i, label in enumerate(names):
        axes[i,i].annotate(label, (0.5, 0.5), xycoords='axes fraction',
                           ha='center', va='center')
        pass

    if title: plt.suptitle(title)
    return fig

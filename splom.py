import itertools

## Code obtained from https://stackoverflow.com/a/7941594
def splom(data, names, plt, np):
    """Plots a scatterplot matrix of subplots.  Each row of "data" is plotted
    against other rows, resulting in a nrows by nrows grid of subplots with the
    diagonal subplots labeled with "names".  Additional keyword arguments are
    passed on to matplotlib's "plot" command. Returns the matplotlib figure
    object containg the subplot grid."""
    nfeatures = len(data)
    fig, axes = plt.subplots(nrows=nfeatures, ncols=nfeatures, figsize=(8,8))
    fig.subplots_adjust(hspace=0.05, wspace=0.05)

    for ax in axes.flat:
        # Hide all ticks and labels
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Set up ticks only on one side for the "edge" subplots...
        if ax.is_first_col():
            ax.yaxis.set_ticks_position('left')
        if ax.is_last_col():
            ax.yaxis.set_ticks_position('right')
            
        if ax.is_first_row():
            ax.xaxis.set_ticks_position('top')
        if ax.is_last_row():
            ax.xaxis.set_ticks_position('bottom')

    # Plot the data.
    for i in range(nfeatures):
        for j in range(nfeatures):
            if i == j: continue

            print 'data[i]:', data[i]
            print 'data[j]:', data[j]
            
            axes[i][j].plot(data[i],data[j],
                            linestyle='none',
                            marker='o', color='black',
                            mfc='none'
            )
            
            pass
        pass
    # for i, j in zip(*np.triu_indices_from(axes, k=1)):
    #     for x, y in [(i,j), (j,i)]:
    #         axes[x,y].plot(data[x], data[y],
    #                        linestyle='none',
    #                        marker='o', color='black',
    #                        mfc='none'
    #                        #**kwargs
    #         )

    # Label the diagonal subplots...
    for i, label in enumerate(names):
        axes[i,i].annotate(label, (0.5, 0.5), xycoords='axes fraction',
                           ha='center', va='center')

    # Turn on the proper x or y axes ticks.
    for i in range(nfeatures):
        axes[0,i].xaxis.set_visible(True)
        axes[i,0].yaxis.set_visible(True)
        pass
    # for i, j in zip(range(nfeatures), itertools.cycle((-1, 0))):
    #     axes[j,i].xaxis.set_visible(True)
    #     axes[i,j].yaxis.set_visible(True)
    #     pass

    return fig

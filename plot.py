import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import os

# set file to be read in
filename = 'output.dat'

#%%
# This path if running the file from shell, i.e. python plot.py
if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print('Your file directory is:', dir_path)
    print('Reading in {} from the relaxation program...'.format(filename))
    df = pd.read_table(os.path.join(dir_path, filename), header=None, delim_whitespace=True)
    print('Data read complete.')
    print('Generating colored graph columns...')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    length = len(df.iloc[:, 2])
    if length < 1000:
        size = 10
    elif length < 10000:
        size = 1
    elif length < 50000:
        size = 0.1
    else:
        size = 0.01
    cax = ax.scatter(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2], c=df.iloc[:, 2], cmap='inferno')
    ax.set_ylabel('$y$')
    ax.set_xlabel('$x$')
    ax.set_zlabel('$z$')
    ax.set_autoscalez_on(True)
    cb = fig.colorbar(cax, orientation='horizontal', fraction=0.05)
    plt.tight_layout()
    plt.savefig(os.path.join(dir_path, 'outputgraph.pdf'), dpi=800)
    print('Graph drawn. See outputgraph.pdf.')

    print('Generating heatmap of columns...')
    f = plt.figure()
    ax = f.add_subplot(111)
    ax.set_ylabel('$y$')
    ax.set_xlabel('$x$')
    cax = ax.hexbin(x=df.iloc[:, 0], y=df.iloc[:, 1], C=df.iloc[:, 2], cmap='inferno')
    cb = f.colorbar(cax)
    cb.set_label('$z$')
    plt.savefig(os.path.join(dir_path, 'heatmap.pdf'), dpi=800)
    print('Heatmap drawn. See heatmap.pdf.')

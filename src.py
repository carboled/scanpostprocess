import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import os
import sys
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib import cm
import time
from pathlib import Path
plt.rc('xtick',labelsize=25)
plt.rc('ytick',labelsize=25)
plt.rc('legend',fontsize= 30)
plt.rc('font',size= 30)

def read_xyz(path_to_scan, cellsize=0.01):
    """
    Read an xyz format file using read_csv function of pandas
    
    Parameters
    ----------
    path_to_scan: str
        String with path to scan
    cellsize: float
        Cell size in meters

    Returns
    --------
    D: xr.DataArray 
        DataArray with x and y as coordinates
    """
    path_to_scan = Path(r"" + path_to_scan)
    print(path_to_scan.is_file())
    a = pd.read_csv(path_to_scan,sep=' ', names=['X', 'Y', 'Z', 'R', 'B', 'G'])#, usecols=[0,1,2])
    b = a.where(a['X']>-0.4).where(a['X']<0.4).where(a['Y']>0).where(a['Y']<1).dropna()
    X = np.linspace(-0.4, 0.4,int(0.8/cellsize))
    Xc = (X[:-1] + X[1:])/2
    Y = np.linspace(0,1,int(1/cellsize))
    Yc = (Y[:-1] + Y[1:])/2
    Yg,Xg = np.meshgrid(Yc,Xc)
    Z = np.array([])
    for lbx,ubx in zip(X[:-1],X[1:]):
        for lby,uby in zip(Y[:-1],Y[1:]):
            xs = b['X'].between(lbx,ubx)
            ys = b['Y'].between(lby,uby)
            Z = np.append(Z,b['Z'][ys&xs].mean())
    Zg = Z.reshape(Xg.shape)
    D = xr.DataArray(Zg, dims=['x','y'],coords=[Xc,Yc])
    return D, Xg, Yg, Zg


def plot_surface_coordinates( Xg, Yg, Zg, name="terrain_coordinates.png"):
    """
    Make a surface plot using meshgrid.
    
    Parameters
    ----------
    Xg:  
    Yg:
    Zg:
    name:

    Returns
    --------
    None
    """
    path_plots = Path("plots")
    path_plots.mkdir(exist_ok=True)
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111, projection='3d')
    mappable = plt.cm.ScalarMappable()
    mappable.set_array(Zg)
    im = ax.plot_surface(Xg, Yg, Zg,cmap=mappable.cmap)
    plt.colorbar(im)
    ax.view_init(elev=30, azim=30)
    plt.savefig('plots/' + name)
    plt.close()

 
def plot_surface_dataarray(D, name="terrain_dataarray.png"):
    """
    Make a surface plot using dataarray.
    
    Parameters
    ----------
    D:
    name:

    Returns
    --------
    None
    """ 
    path_plots = Path("plots")
    path_plots.mkdir(exist_ok=True)
    D.plot.surface()
    plt.savefig('plots/' + name)
    plt.close()


def plot_profiles(D, name="profile.png"):
    """
    Make a profiles plot using dataarray.
    
    Parameters
    ----------
    D:  
    name:

    Returns
    --------
    None
    """
    path_plots = Path("plots")
    path_plots.mkdir(exist_ok=True)
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111)
    locations = [-0.3, -0.15,0, 0.15, 0.3]
    for loc in locations:
        D.interp(x=[loc]).plot(label = 'x ='+str(loc))
    plt.title('Profiles')
    plt.legend(title='Legend')
    plt.savefig('plots/'+name)
    plt.close()

if __name__ == "__main__":
    start = time.time()
    cellsize = 0.01
    path_to_scan = sys.argv[1]
    D, Xg, Yg, Zg = read_xyz(path_to_scan, cellsize=0.01)
    plot_surface_coordinates( Xg, Yg, Zg)
    plot_surface_dataarray(D)
    plot_profiles(D)
    stop = time.time()
    print(stop-start)
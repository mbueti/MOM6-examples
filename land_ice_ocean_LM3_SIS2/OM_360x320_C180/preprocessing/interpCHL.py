#!/usr/bin/env python

from midas.rectgrid import *
import netCDF4 as nc
import numpy as np

sgrid=supergrid(file='ocean_hgrid.nc')
grid=quadmesh(supergrid=sgrid,cyclic=True)
ogrid=quadmesh('/archive/gold/datasets/global/siena_201204/INPUT/seawifs_1998-2006_GOLD_smoothed_2X.nc',var='CHL_A',cyclic=True)
O=state('/archive/gold/datasets/global/siena_201204/INPUT/seawifs_1998-2006_GOLD_smoothed_2X.nc',grid=ogrid,fields=['CHL_A'])
O.var_dict['CHL_A']['Z']=None
OM=O.horiz_interp('CHL_A',target=grid,method='bilinear')
print OM.CHL_A.shape
print O.var_dict['CHL_A']['T']
OM.rename_field('CHL_A','chl_a')
OM.var_dict['chl_a']['xax_data']=grid.x_T[0,:]
OM.var_dict['chl_a']['yax_data']=grid.y_T[:,grid.im/4]
OM.write_nc('seawifs_1998-2006_smoothed_2X.nc',fields=['chl_a'])

import pandas as pd
import numpy as np
import re
from sortDataNew import sortData
from datetime import datetime, timedelta
from satellitePositions import get_satellite_positions
from computebaner import runData
import rasterio
from datetime import datetime
#"python": "python -u",
position = (7053759,173158) # tuple of N, E
latlon = (63.29589, 8.83329)
#print(np.cos(120*np.pi/180))
path ='../DOM1_11-14_UTM33_20211217/33-'

def UTMtilRastercelle(N,E):

    indexboundsN = range(140,145)
    indexboundsE = range(114,119)

    bottom = 7026000.0
    left=110430.0

    index_N = 140
    index_E = 114
    
    sidelength = 15000

    N = N - bottom
    E = E - left
    #print(N,E)
    #print(N//sidelength)
    #print(E//sidelength)

    index_N += N//sidelength
    index_E += E//sidelength
    filename = f'{path}{int(index_E)}-{int(index_N)}.tif'
    index = (sidelength+5-int(N-N//sidelength*sidelength),5+int(E-E//sidelength*sidelength))
    if index_N in indexboundsN and index_E in indexboundsE:
        return filename,index
    else:
        raise Exception('Index out of bounds, no tif file for these UTM coordinates')



def filterTerrain(df, position):

    """
    Input: Takes a list of list of dataframes consisting of Id, time, cartesian position (X,Y,Z), azimuth and zenith.

    Output: Dataframe of satellites not blocked by the terrain at the checked coordinate, same dimension as the input.
    """
    starttime = datetime.now()
    print('FilterTerrain Start')
    elevation_mask = 10

    filename, cell_index = UTMtilRastercelle(position[0],position[1])
    print(cell_index,'cell index')
    dataset = rasterio.open(filename)
    data = dataset.read(1)
    epochs = []
    distance_count = 0
    satellites = df
    max_height = 0
    for epoch in satellites:
        sat_types = []

        for gnss_type in epoch:
            sats = []
            for index, gnss in gnss_type.iterrows():
                N = position[0]
                E = position[1]
                N_cell = cell_index[1]
                E_cell = cell_index[0]

                baseheight = data[E_cell][N_cell]
                #print(baseheight,'baseheight')
                angle = ((gnss['azimuth']-90)%360)*np.pi/180
                N_step = np.cos(angle)
                E_step = np.sin(angle)
                #print(gnss['zenith'],'zenith',angle*180/np.pi)
                obsangle = 0
                while obsangle < gnss['zenith']:
                    
                    N_prev = N
                    E_prev = E
                    N += N_step
                    E += E_step

                    #if int(N)%2 == 0:
                       #N_cell += int(np.sign(N-position[0]))
                    #if int(E)%2 == 0:
                        #E_cell += int(np.sign(E-position[1]))
                    N_cell += int(N)-int(N_prev)
                    E_cell += int(E)-int(E_prev)

                    if N_cell < 0 or N_cell > 15010 or E_cell < 0 or E_cell > 15010:
                        print('Out of Raster bounds')
                        break

                
                    height = data[E_cell][N_cell]
                    #if height > max_height:
                    #    max_height = height
                    distance = np.sqrt((N-position[0])**2+(E-position[1])**2)
                    
                    obsangle = np.arctan((height-baseheight)/distance)*180/np.pi
                    #if gnss['zenith'] < obsangle:
                    #    print('hei')
                    #    break
                    #print(obsangle)
                    if distance > 5000: # Distance in meters
                        #Satellite is visible
                        #add gnss to new dataframe
                        distance_count += 1
                        sats.append(gnss)
                        obsangle = 90
                #print(max_obsangle,'max obsangle')
            sat_types.append(sats)
        epochs.append(sat_types)
    print(distance_count)
    print(max_height)
    print(datetime.now()-starttime, 'time')
    return epochs

    #print(satellite)

test = runData(['GPS'], '10', '2025-03-04T12:00:00.000', 1)
result = filterTerrain(test[1], position)
nono = 0
for i in test[1]:
    for j in i:
        for k in j.iterrows():
            nono += 1
print(nono)
#print(test[1])
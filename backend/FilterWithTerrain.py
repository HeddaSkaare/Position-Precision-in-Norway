import pandas as pd
import numpy as np
import re
from sortDataNew import sortData
from datetime import datetime, timedelta
from satellitePositions import get_satellite_positions
from computebaner import runData
#"python": "python -u",
position = (7032447, 178496) # tuple of N, E
latlon = (63.29589, 8.83329)


def UTMtilRastercelle(N,E):

    indexboundsN = range(140,145)
    indexboundsE = range(114,119)

    bottom = 7025995.0
    left=110425.0

    index_N = 140
    index_E = 114
    
    sidelength = 15000

    N = N - bottom
    E = E -left
    print(N,E)
    print(N//sidelength)
    print(E//sidelength)

    index_N += N//sidelength
    index_E += E//sidelength
    filename = f'DOM1_11-14_UTM33_20211217/33-{int(index_E)}-{int(index_N)}.tif'
    index = (N-N//sidelength*sidelength,E-E//sidelength*sidelength)
    if index_N in indexboundsN and index_E in indexboundsE:
        return filename,index
    else:
        raise Exception('Index out of bounds, no tif file for these UTM coordinates')



def filterTerrain(df, position):

    """
    Input: Takes a list of list of dataframes consisting of Id, time, cartesian position (X,Y,Z), azimuth and zenith.

    Output: Dataframe of satellites not blocked by the terrain at the checked coordinate, same dimension as the input.
    """

    elevation_mask = 10

    filename, cell_index = UTMtilRastercelle(position[0],position[1])

    satellites = df
    for epoch in satellites:
        for gnss_type in epoch:
            for index, gnss in gnss_type.iterrows():

                baseheight = data[cell_index[0],cell_index[1]]
                print(gnss['azimuth'])
                angle = (gnss['azimuth']-90)%360
                obsangle = 0
                while obsangle < gnss['zenith']:

                    cell_index[0]+=1
                    cell_index[1]+=np.sin(angle)
                    height = data[int(cell_index[0]),int(cell_index[1])]
                    distance = np.sqrt(int(cell_index[0]-position[0])**2+int(cell_index[1]-position[1])**2)
                    obsangle = (height-baseheight)/distance

                    if distance > 750:
                        #Satellite is visible
                        #add gnss to new dataframe
                        obsangle = 90


                break
            break
        break


    #print(satellite)
#print('hei')
test = runData(['GPS', 'Galileo', 'GLONASS', 'BeiDou'], '10', '2025-02-12T12:00:00.000', 4)
filterTerrain(test[1], position)
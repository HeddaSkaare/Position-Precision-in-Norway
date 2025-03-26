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
position = (124657.85,6957624.16) # tuple of E,N
#latlon = (63.29589, 8.83329)
#print(np.cos(120*np.pi/180))
path ='DOM10_UTM33_20250228'

# dataset = rasterio.open(f'DOM10_UTM33_20250228/6400_1_10m_z33.tif')
# print(dataset.name)
# print(dataset.bounds)

# (49745.0,6500255)
# print(N_cell,E_cell)

#print(dataset.crs)
#data = dataset.read(1)
#print(data.shape)
#print(data[5051])



def UTMtilRaster(E,N):
    
    sidelength = 50000 # 510 meters of overlap
    E, N = int(E), int(N)
    oldN = N
    oldE = E
    

    left = -255
    bottom = 6399745

    N -= bottom
    E -= left

    N_index = N//(sidelength*2)
    E_index = E//(sidelength*2)

    N -= N_index*(sidelength*2)
    E -= E_index*(sidelength*2)
    

    if E > sidelength and N > sidelength:
        quad = '1'
    elif E > sidelength and N < sidelength:
        quad = '2'
    elif E < sidelength and N < sidelength:
        quad = '3'
    elif E < sidelength and N > sidelength:
        quad = '4'
    
    N_index += 64

    if oldE < -255:
        filename = f'{path}/{N_index}m1_{quad}_10m_z33.tif'
    else:
        filename = f'{path}/{N_index}{E_index:02d}_{quad}_10m_z33.tif'

    return filename


def filterTerrain(df, position):

    """
    Input: Takes a list of list of dataframes consisting of Id, time, cartesian position (X,Y,Z), azimuth and zenith.

    Output: Dataframe of satellites not blocked by the terrain at the checked coordinate, same dimension as the input.
    """
    starttime = datetime.now()
    print('FilterTerrain Start')
    elevation_mask = 10

    filename = UTMtilRaster(position[0],position[1])
    step_size = 5

    dataset = rasterio.open(filename)
    N_start, E_start = dataset.index(position[0],position[1])

    datas = []
    datas.append(dataset.read(1))
    epochs = []
    distance_count = 0
    angle_count = 0
    satellites = df
    max_height = 0
    baseheight = datas[0][E_start][N_start]
    for epoch in satellites:
        sat_types = []

        for gnss_type in epoch:
            sats = []
            for index, gnss in gnss_type.iterrows():
                
                N = position[1]
                E = position[0]
                
                data_index = 0

                angle = ((gnss['azimuth']-90)%360)*np.pi/180
                
                N_step = np.cos(angle)*step_size
                E_step = np.sin(angle)*step_size
                obsangle = 0
                distance = 0
                data_index = 0

                while obsangle < gnss['zenith']:
                    
                    
                    N += N_step
                    E += E_step
                    
                    N_cell, E_cell = dataset.index(E,N)

                    if N_cell < 0 or N_cell >= 5051 or E_cell < 0 or E_cell >= 5051:
                        filename = UTMtilRaster(int(E),int(N))
                        dataset = rasterio.open(filename)
                        datas.append(dataset.read(1))
                        N_cell, E_cell = dataset.index(E,N)
                        data_index = 1
                        
                    height = datas[data_index][E_cell][N_cell]
                    distance += step_size #np.sqrt((N-position[1])**2+(E-position[0])**2)

                    obsangle = np.arctan((height-baseheight)/distance)*180/np.pi

                    if abs(distance) > 5000: # Distance in meters
                        distance_count += 1
                        sats.append(gnss)
                        obsangle = 90
            sats = pd.DataFrame(sats,columns=['Satelitenumber', 'time', 'X','Y','Z','azimuth', 'zenith'])
            sat_types.append(sats)
        epochs.append(sat_types)
    #print(distance_count,'distance count')
    print('FilterTerrain End ',datetime.now()-starttime, ' time')
    return epochs

    #print(satellite)

test = runData(['GPS','Galileo'], '10', '2025-03-22T08:00:00.000', 0)
result = filterTerrain(test[1], position)
#nono = 0
print(result)
print(test[1])
# for i in test[1]:
#    for j in i:
#        for k in j.iterrows():
#            print(k)
#print(nono,'nono')
#print(test[1])


# Med index 0:00:08.656879 time
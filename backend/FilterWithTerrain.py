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
#position = (173158,7053759) # tuple of E,N
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

    oldN = N
    oldE = E
    

    left = -255
    bottom = 6399745
    #print(E,N)
    N -= bottom
    E -= left

    #print(E,N)

    N_index = N//(sidelength*2)
    E_index = E//(sidelength*2)
    #print(E, type(E))

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
    #print(N_index,E_index,quad)
    #quad = int(quad,2)+1

    

    #print(N_index,E_index,quad)

    if oldE < -255:
        filename = f'{path}/{N_index}m1_{quad}_10m_z33.tif'
    else:
        filename = f'{path}/{N_index}{E_index:02d}_{quad}_10m_z33.tif'

    #print(filename)
    
    

    return filename

"""
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

"""

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
    #print(filename)
    dataset = rasterio.open(filename)
    N_start, E_start = dataset.index(position[0],position[1])
    #print(N_cell,E_cell)
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

                
                #print(baseheight,'baseheight')
                angle = ((gnss['azimuth']-90)%360)*np.pi/180
                
                N_step = np.cos(angle)*step_size
                E_step = np.sin(angle)*step_size
                #print(gnss['zenith'],'zenith',angle*180/np.pi)
                obsangle = 0
                #N_prev = N
                #E_prev = E
                distance = 0
                data_index = 0

                #N_cell_old = N_cell
                #E_cell_old = E_cell

                while obsangle < gnss['zenith']:
                    
                    
                    N += N_step
                    E += E_step

                    #if int(N)%2 == 0:
                       #N_cell += int(np.sign(N-position[0]))
                    #if int(E)%2 == 0:
                        #E_cell += int(np.sign(E-position[1]))
                    #N_cell = int((N-N_prev)/10)+N_cell_old
                    #E_cell = int((E-E_prev)/10)+E_cell_old
                    
                    N_cell, E_cell = dataset.index(E,N)
                    #print(N_cell,E_cell)
                    if N_cell < 0 or N_cell >= 5051 or E_cell < 0 or E_cell >= 5051:
                        #print('Out of Raster bounds')
                        #print(E,N)
                        #print(N_cell,E_cell)
                        filename = UTMtilRaster(int(E),int(N))
                        #print(filename)
                        dataset = rasterio.open(filename)
                        #print(dataset.bounds)
                        datas.append(dataset.read(1))
                        N_cell, E_cell = dataset.index(E,N)
                        #N_cell_old = N_cell
                        #E_cell_old = E_cell
                        #print(N_cell,E_cell)
                        data_index = 1
                        

                
                    height = datas[data_index][E_cell][N_cell]
                    #if height > max_height:
                    #    max_height = height
                    distance += step_size #np.sqrt((N-position[1])**2+(E-position[0])**2)
                    #print(distance)
                    obsangle = np.arctan((height-baseheight)/distance)*180/np.pi
                    #if gnss['zenith'] < obsangle:
                    #   angle_count += 1
                    #print(obsangle)
                    if abs(distance) > 5000: # Distance in meters
                        #Satellite is visible
                        #add gnss to new dataframe
                        #print(distance)
                        distance_count += 1
                        sats.append(gnss)
                        obsangle = 90
                #print(max_obsangle,'max obsangle')
                #print('next satellite')
            sats = pd.DataFrame(sats,columns=['Satelitenumber', 'time', 'X','Y','Z','azimuth', 'zenith'])
            sat_types.append(sats)
        #sat_types = pd.DataFrame(sat_types)
        epochs.append(sat_types)
    print(distance_count,'distance count')
    #print(angle_count,'angle count')
    #print(max_height)
    print('FilterTerrain End')
    print(datetime.now()-starttime, 'time')
    return epochs

    #print(satellite)

#test = runData(['GPS','Galileo'], '10', '2025-03-04T12:00:00.000', 1)
#result = filterTerrain(test[1], position)
#nono = 0
#print(result)
# for i in test[1]:
#    for j in i:
#        for k in j.iterrows():
#            print(k)
#print(nono,'nono')
#print(test[1])


# Med index 0:00:08.656879 time
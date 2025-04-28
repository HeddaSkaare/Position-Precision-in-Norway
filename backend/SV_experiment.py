import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Transformer
from sortDataNew import sortData
import datetime
from satellitePositions import get_satellite_positions
from generateElevationMask import check_satellite_sight, check_satellite_sight_2
from computebaner import  get_gnss, getDayNumber, runData_check_sight,runData_no_terrain,visualCheck_no_terrain
from computeDOP import best, find_dop_on_point
from common_variables import wgs
import time
from pyubx2 import UBXReader, UBXMessage, UBX_PROTOCOL, NMEA_PROTOCOL, RTCM3_PROTOCOL
time_start = time.time()
def read_ubx(filepath):
    with open(filepath, 'rb') as stream:
        ubr = UBXReader(stream, protfilter=NMEA_PROTOCOL)
        teller = 0
        #11:24:03
        #11:27:45
        data = {}
        timer = 0
        teller2 = 0
        tim = 0
        for raw_data, parsed_data in ubr:
            
            if parsed_data.identity == 'GNRMC':
                if tim:
                    sat_count = np.zeros(4)
                    for i in sorted(set(sats)):
                        if i[0] == 'G':
                            sat_count[0] += 1
                        elif i[0] == 'R':
                            sat_count[1] += 1
                        elif i[0] == 'E':
                            sat_count[2] += 1
                        elif i[0] == 'C':
                            sat_count[3] += 1
                    data[tim] = [tim,lat,lon,sorted(set(sats)),sat_count,dt]
                add = False
                timer+=1
                teller2 +=1
                tim = 0
                if timer == 60: # Sjekker hvert minutt
                    add = True
                    tim = parsed_data.time
                    dt = datetime.datetime.combine(parsed_data.date,parsed_data.time)
                    lat = parsed_data.lat
                    lon = parsed_data.lon
                    sats = []
                    timer = 0
                    
            if parsed_data.identity == 'GPGSV' and add:
                for i in range(1,5):
                    
                    try:
                        
                        attr = 'svid_0' + str(i)

                        id  = getattr(parsed_data, attr)
                        sats.append('G'+f"{id:02d}")
                        
                    except AttributeError:
                        
                        pass
            if parsed_data.identity == 'GLGSV' and add:
                for i in range(1,5):
                    try:
                        attr = 'svid_0' + str(i)

                        id  = getattr(parsed_data, attr)
                        try:
                            sats.append('R'+f"{(id-64):02d}")
                            
                        except:
                            pass
                    except AttributeError:
                        pass
            if parsed_data.identity == 'GAGSV' and add:
                for i in range(1,5):
                    try:
                        attr = 'svid_0' + str(i)

                        id  = getattr(parsed_data, attr)
                        sats.append('E'+f"{id:02d}")
                        
                    except AttributeError:
                        pass
            if parsed_data.identity == 'GBGSV' and add:
                for i in range(1,5):
                    try:
                        attr = 'svid_0' + str(i)

                        id  = getattr(parsed_data, attr)
                        sats.append('C'+f"{id:02d}")
                              
                    except AttributeError:
                        pass
    return data, sat_count
#print(read_ubx('Ned Romsdalen.ubx'))
data, sat_count = read_ubx('data/Ned Romsdalen.ubx')
print(time.time()-time_start)
a = datetime.time(10,40,46)
gnss = ['GPS','GLONASS','Galileo','BeiDou'] # This order is hardcoded in the function
count = 0
tida = []
exp = []
res = []
for key, value in data.items():
    
    count += 1
    if count == 95:
        print('hei')
        vis_sat_df = runData_check_sight(gnss, 0, '2025-03-30T'+str(key)+'.000', 0, [value[2],value[1]])[1]
        tida.append(value[-1])
        #print(value[2],value[1],'hallo')
        res.append(sum(len(vis_sat_df[0][i]) for i in range(len(vis_sat_df[0]))))
        exp.append(sum(value[4]))
        # for i in range(len(vis_sat_df[0])):
        #     print(len(vis_sat_df[0][i]),value[4][i])
        # #print(vis_sat_df)
        # print(value[3])
        # print('---------------------------------------------------------------')
plt.plot(tida,res,label='Expected satellites')
plt.plot(tida,exp,label='Visible satellites')
        
#vis_sat_df = runData_no_terrain(gnss, 0, '2025-03-30T10:46:46.000', 0, [7.6976858333, 62.5347858333],46)[1]
#print(vis_sat_df)
#2025-03-13T12:00:00.000
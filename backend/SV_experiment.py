import pandas as pd
import numpy as np
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
        teller = 0
        teller2 = 0
        tim = 0
        for raw_data, parsed_data in ubr:
            
            if parsed_data.identity == 'GNRMC':
                if tim:
                    data[tim] = [tim,lat,lon,sorted(set(sats))]
                add = False
                teller+=1
                teller2 +=1
                tim = 0
                if teller == 60:
                    add = True
                    tim = parsed_data.time
                    lat = parsed_data.lat
                    lon = parsed_data.lon
                    sats = []
                    teller = 0
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
    return data
#print(read_ubx('Ned Romsdalen.ubx'))
data = read_ubx('data/Ned Romsdalen.ubx')
print(time.time()-time_start)
a = datetime.time(10,40,46)
gnss = ['GPS','GLONASS','Galileo','BeiDou']
count = 0
for key, value in data.items():
    
    count += 1
    if count == 100:
        vis_sat_df = runData_check_sight(gnss, 0, '2025-03-30T'+str(key)+'.000', 0, [value[2],value[1]])[1]
        print(value[0])
        print(value[2],value[1])
        print(vis_sat_df)
        print(value[3])
        print('---------------------------------------------------------------')
        
        
#vis_sat_df = runData_check_sight(gnss, 0, '2025-03-30T'+a+'.000', 0, [9.0,62.0])[1]
#print(vis_sat_df)
#2025-03-13T12:00:00.000
import math
import pandas as pd
import numpy as np
import re
import ahrs
from datetime import datetime
import os
import gzip
import shutil
from downloadfile import lastned

# G: GPS
# R: GLONASS
# E: Galileo
# J: QZSS
# C: BDS
# I: NavIC/IRNSS
# S: SBAS payload
columnsG = [
    "type",
    "satelite_id",
    "Datetime",
    "C_rs",
    "Delta n0",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "t_tm",
]
columnsR = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "X",
    "Vx",
    "ax",
    "Health",
    "Y",
    "Vy",
    "ay",
    "Frequency number",
    "Z",
    "Vz",
    "az",
    "Age of operation",
]

def split_on_second_sign(s):
    signs = [m.start() for m in re.finditer(r'(?<![eE])[+-]', s)]
    if not signs:
        return s

    parts = []
    last_index = 0
    for idx in signs:
        parts.append(s[last_index:idx])  
        last_index = idx 
    parts.append(s[last_index:])
    
    return parts

def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            flat_list.extend(item)  
        else:
            flat_list.append(item) 
    return flat_list

def strToFloat(inputstring):
    splittedString = inputstring.split("e")
    num = float(splittedString[0])
    potens = int(splittedString[1])
    return num * 10**potens

def GPSdata(df,satellitt_id,time, values_list, SV,type):
    if type == 'LNAV':
        df.loc[len(df)]  = [
            type,
            satellitt_id,
            time,
            values_list[1],
            values_list[2],
            values_list[3],
            values_list[4],
            values_list[5],
            values_list[6],
            values_list[7],
            values_list[8],
            values_list[9],
            values_list[10],
            values_list[11],
            values_list[12],
            values_list[13],
            values_list[14],
            values_list[15],
            values_list[16],
            values_list[24],
        ]
    # if type == 'CNAV':
    #     df.loc[len(df)]  = [
    #         type,
    #         satellitt_id,
    #         time,
    #         values_list[1],
    #         values_list[2],
    #         values_list[3],
    #         values_list[4],
    #         values_list[5],
    #         values_list[6],
    #         values_list[7],
    #         values_list[8],
    #         values_list[9],
    #         values_list[10],
    #         values_list[11],
    #         values_list[12],
    #         values_list[13],
    #         values_list[14],
    #         values_list[15],
    #         values_list[16],
    #         values_list[28],
    #     ]
    # elif type == 'CNV2':
    #     df.loc[len(df)]  = [
    #         type,
    #         satellitt_id,
    #         time,
    #         values_list[1],
    #         values_list[2],
    #         values_list[3],
    #         values_list[4],
    #         values_list[5],
    #         values_list[6],
    #         values_list[7],
    #         values_list[8],
    #         values_list[9],
    #         values_list[10],
    #         values_list[11],
    #         values_list[12],
    #         values_list[13],
    #         values_list[14],
    #         values_list[15],
    #         values_list[16],
    #         values_list[30],
    #     ]
def GLONASSdata(df,satellitt_id,time, values_list, SV,type):
    df.loc[len(df)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11]
    ]
columnsE = [
    "satelite_id",
    "Datetime",
    "C_rs",
    "Delta n0",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "Data source",
    "GAL Week",
    "SISA signal",
    "SV health",
    "BGDa",
    "BGDb",
    "t_tm"
]

def Galileiodata(df,satellitt_id,time, values_list, SV,type):#type is the same
    df.loc[len(df)] = [
        satellitt_id,
        time,
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11],
        values_list[12],
        values_list[13],
        values_list[14],
        values_list[15],
        values_list[16],
        values_list[17],
        values_list[18],
        values_list[20],
        values_list[21],
        values_list[22],
        values_list[23],
        values_list[24]
    ]
columnsJ = [
    "type",
    "satelite_id",
    "Datetime",
    "C_rs",
    "Delta n0",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "t_tm",
]
def QZSSdata(df,satellitt_id,time, values_list, SV,type):
    if type == 'LNAV':
        df.loc[len(df)] = [
            type,
            satellitt_id,
            time,
            values_list[1],
            values_list[2],
            values_list[3],
            values_list[4],
            values_list[5],
            values_list[6],
            values_list[7],
            values_list[8],
            values_list[9],
            values_list[10],
            values_list[11],
            values_list[12],
            values_list[13],
            values_list[14],
            values_list[15],
            values_list[16],
            values_list[24],
        ]
    elif type == 'CNAV':
        df.loc[len(df)] = [
            type,
            satellitt_id,
            time,
            values_list[1],
            values_list[2],
            values_list[3],
            values_list[4],
            values_list[5],
            values_list[6],
            values_list[7],
            values_list[8],
            values_list[9],
            values_list[10],
            values_list[11],
            values_list[12],
            values_list[13],
            values_list[14],
            values_list[15],
            values_list[16],
            values_list[28],
        ]
    elif type == 'CNV2':
        df.loc[len(df)] = [
            type,
            satellitt_id,
            time,
            values_list[1],
            values_list[2],
            values_list[3],
            values_list[4],
            values_list[5],
            values_list[6],
            values_list[7],
            values_list[8],
            values_list[9],
            values_list[10],
            values_list[11],
            values_list[12],
            values_list[13],
            values_list[14],
            values_list[15],
            values_list[16],
            values_list[30],
        ]
columnsC = [
    "type",
    "satelite_id",
    "Datetime",
    "C_rs",
    "Delta n0",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "t_tm",

]
def BeiDoudata(df,satellitt_id,time, values_list, SV,type):
    if type == 'D1' or type == 'D2':
        df.loc[len(df)] = [
            type,
            satellitt_id,
            time,
            values_list[1],
            values_list[2],
            values_list[3],
            values_list[4],
            values_list[5],
            values_list[6],
            values_list[7],
            values_list[8],
            values_list[9],
            values_list[10],
            values_list[11],
            values_list[12],
            values_list[13],
            values_list[14],
            values_list[15],
            values_list[16],#idot
            values_list[24],#tm

        ]
    elif type == 'CNV1' or type == 'CNV2':
        df.loc[len(df)] = [
            type,
            satellitt_id,
            time,
            values_list[1],
            values_list[2],
            values_list[3],
            values_list[4],
            values_list[5],
            values_list[6],
            values_list[7],
            values_list[8],
            values_list[9],
            values_list[10],
            values_list[11],
            values_list[12],
            values_list[13],
            values_list[14],
            values_list[15],
            values_list[16],#idot
            values_list[31],
        ]
    elif type == 'CNV3':
        df.loc[len(df)] = [
            type,
            satellitt_id,
            time,
            values_list[1],
            values_list[2],
            values_list[3],
            values_list[4],
            values_list[5],
            values_list[6],
            values_list[7],
            values_list[8],
            values_list[9],
            values_list[10],
            values_list[11],
            values_list[12],
            values_list[13],
            values_list[14],
            values_list[15],
            values_list[16],#idot
            values_list[28],
        ]
columnsI =  [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "IODEC",
    "C_rs",
    "Delta n0",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "Spare1",
    "IRN Week",
    "Spare2",
    "User Range accurracy",
    "Health",
    "TGD",
    "Spare3",
    "t_tm"
]
def NavICdata(df,satellitt_id,time, values_list, SV, type):
    df.loc[len(df)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11],
        values_list[12],
        values_list[13],
        values_list[14],
        values_list[15],
        values_list[16],
        values_list[17],
        values_list[18],
        values_list[19],
        values_list[20],
        values_list[21],
        values_list[22],
        values_list[23],
        values_list[24]
    ]
columnsS =[
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "X",
    "Vx",
    "ax",
    "Health",
    "Y",
    "Vy",
    "ay",
    "Accurracy code",
    "Z",
    "Vz",
    "az",
    "IODN"
]
def SBASdata(df,satellitt_id,time, values_list, SV, type):
    df.loc[len(df)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11]
    ]

def update_navigation_message_type(df):
    """
    Update the navigation message type for each satellite ID to the last type encountered.
    """
    result_list = []
    for sat_id, sat_group in df.groupby('satelite_id'):
        last_type = sat_group['type'].iloc[-1]
        # Get the last type for each satellite ID
        filtered = sat_group[sat_group['type'] == last_type]
        result_list.append(filtered)
        
    new_df = pd.concat(result_list, ignore_index=True)
    return new_df

def sortData(daynumber, date):

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    output_folder = os.path.join(CURRENT_DIR, "DataFrames", str(date.year), str(daynumber))
    file_pathG = os.path.join(output_folder, "structured_dataG.csv")

    if os.path.exists(file_pathG):
        print(f"Data on day {daynumber} already sorted")
        return
    else:
        # ---- Last ned og pakk ut ----
        filename = f'BRD400DLR_S_{date.year}{daynumber}0000_01D_MN.rnx'
        # Bruk full sti til fila som skal leses
        filepath = os.path.join(CURRENT_DIR, "unzipped", filename)

        lastned(daynumber, date.year)

        current_date = date.date()

        structured_dataG = pd.DataFrame(columns=columnsG)
        structured_dataR = pd.DataFrame(columns=columnsR)
        structured_dataE = pd.DataFrame(columns=columnsE)
        structured_dataJ = pd.DataFrame(columns=columnsJ)
        structured_dataC = pd.DataFrame(columns=columnsC)
        structured_dataI = pd.DataFrame(columns=columnsI)
        structured_dataS = pd.DataFrame(columns=columnsS)

        with open(filepath, "r") as file:
            print(f"Reading file {filepath}")
            content = file.read()

        split_index = content.index("END OF HEADER")
        header_part = content[:split_index]
        data_part = content[split_index+13:]

        satellitt_data = re.split(r'\s*> EPH\s*', data_part)
        print(len(satellitt_data))

        for i in range(1, len(satellitt_data)-1):
            lines = satellitt_data[i].strip().splitlines()
            satellitt_id = lines[0].split(' ')[0]
            type = lines[0].split()[1]

            flattened_forstelinje = flatten(list(map(split_on_second_sign, lines[1].split()[1:])))
            cleaned_forstelinje = [item for item in flattened_forstelinje if item != '']

            values_lines = lines[2:]
            values_list = []
            for line in values_lines:
                flattenedLine = flatten(list(map(split_on_second_sign, line.split())))
                cleanedLine = [item for item in flattenedLine if item != '']
                while len(cleanedLine) < 4:
                    cleanedLine.append(np.nan)
                values_list += cleanedLine

            time = datetime(int(cleaned_forstelinje[0]), int(cleaned_forstelinje[1]),
                            int(cleaned_forstelinje[2]), int(cleaned_forstelinje[3]),
                            int(cleaned_forstelinje[4]), int(cleaned_forstelinje[5]))

            SV = cleaned_forstelinje[6:]

            for i in range(len(SV)):
                SV[i] = strToFloat(SV[i])
            for j in range(len(values_list)):
                if isinstance(values_list[j], str):
                    values_list[j] = strToFloat(values_list[j])

            if time.date() == current_date:
                if "G" in satellitt_id:
                    GPSdata(structured_dataG, satellitt_id, time, values_list, SV, type)
                elif "R" in satellitt_id:
                    GLONASSdata(structured_dataR, satellitt_id, time, values_list, SV, type)
                elif "J" in satellitt_id:
                    QZSSdata(structured_dataJ, satellitt_id, time, values_list, SV, type)
                elif "C" in satellitt_id:
                    BeiDoudata(structured_dataC, satellitt_id, time, values_list, SV, type)
                elif "I" in satellitt_id:
                    NavICdata(structured_dataI, satellitt_id, time, values_list, SV, type)
                elif "S" in satellitt_id:
                    SBASdata(structured_dataS, satellitt_id, time, values_list, SV, type)
                elif "E" in satellitt_id:
                    Galileiodata(structured_dataE, satellitt_id, time, values_list, SV, type)

        print(f"Processing at {time}")

        # Oppdater navigation type for noen systemer
        structured_dataJ = update_navigation_message_type(structured_dataJ)
        structured_dataC = update_navigation_message_type(structured_dataC)

        # ✅ Lag mappe hvis den ikke finnes
        os.makedirs(output_folder, exist_ok=True)

        # ✅ Lagre CSV-er med full sti
        structured_dataG.sort_values(by=['satelite_id', 'Datetime']).to_csv(os.path.join(output_folder, "structured_dataG.csv"), index=False)
        structured_dataR.sort_values(by=['satelite_id', 'Datetime']).to_csv(os.path.join(output_folder, "structured_dataR.csv"), index=False)
        structured_dataE.sort_values(by=['satelite_id', 'Datetime']).to_csv(os.path.join(output_folder, "structured_dataE.csv"), index=False)
        structured_dataJ.sort_values(by=['satelite_id', 'Datetime']).to_csv(os.path.join(output_folder, "structured_dataJ.csv"), index=False)
        structured_dataC.sort_values(by=['satelite_id', 'Datetime']).to_csv(os.path.join(output_folder, "structured_dataC.csv"), index=False)
        structured_dataI.sort_values(by=['satelite_id', 'Datetime']).to_csv(os.path.join(output_folder, "structured_dataI.csv"), index=False)
        structured_dataS.sort_values(by=['satelite_id', 'Datetime']).to_csv(os.path.join(output_folder, "structured_dataS.csv"), index=False)

    
#sortData('099', datetime(2025, 4, 9, 0, 0))
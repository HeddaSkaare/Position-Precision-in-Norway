import json

from matplotlib import pyplot as plt
import numpy as np
import gnsstoolbox.orbits as orbits
import pandas as pd

# # Opprett en instans av Orbit-klassen
# orb = orbits.orbit()
# dataframe = pd.read_csv(f"DataFrames/2025/100/structured_dataR.csv")
# gv = dataframe.iloc[0]
# #"2025-04-10T00:30:00"
# # Legg til GLONASS-navigasjonsdata
# def datetime_to_mjd(dt):
#     JD = dt.toordinal() + 1721424.5 + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24
#     return JD - 2400000.5

# #gv['Datetime'] = pd.to_datetime(gv['Datetime'])
# orb.NAV_dataR.append({
#     'PRN': gv['satelite_id'],
#     'epoch': pd.to_datetime(gv['Datetime']),
#     'X': gv['X'],                      # ECEF PZ-90.11 (meter)
#     'Y': gv['Y'],                      # ECEF PZ-90.11 (meter)
#     'Z': gv['Z'],                      # ECEF PZ-90.11 (meter)
#     'X_dot': gv['Vx'],                    # ECEF PZ-90.11 (m/s)
#     'Y_dot': gv['Vy'],                    # ECEF PZ-90.11 (m/s)
#     'Z_dot': gv['Vz'], 
#     'MS_X_acc': gv['ax'],                # ECEF PZ-90.11 (m/s²)    
#     'MS_Y_acc': gv['ay'],                # ECEF PZ-90.11 (m/s²)
#     'MS_Z_acc': gv['az'],                # ECEF PZ-90.11 (m/s²)
#     'SV_clock_offset': gv['a0'],                # Klokkeavvik (sekunder)
#     'SV_relat_freq_offset': gv['a1'],            # Frekvensavvik (dimensjonsløs)
#     'Message_frame_time': gv['a2'],                    # Referansetidspunkt for ephemeride (sekunder siden ukestart)                   # Tidspunkt for klokkeparametere (sekunder siden ukestart)
#     'sv_health': gv['Health'],
#     'freq_num': gv['Frequency number'],   
#     'age_op_inf': gv['Age of operation'], # Alder på informasjonen (sekunder)          
# })
# # Beregn satellittposisjon på ønsket tidspunkt

# mjd = datetime_to_mjd(pd.to_datetime('2025-04-10T00:29:00'))
# X, Y, Z, dte = orb.calcSatCoord('R',gv['satelite_id'],pd.to_datetime('2025-04-10T00:14:00'),None)
# print(X, Y, Z, dte)
# print(orb.NAV_dataR)
# print('MJD:', mjd)

#sammenligne konstellasjoner
# all_data = []
# gps_data = []
# gpsGalileo_data = []
# gpsGalileoBeidou_data = []
# gpsGalieoGlonass_data = []
# with open('dop_dataAll.json', 'r') as f:
#     data = json.load(f)
#     all_data = data[1]
#     f.close()
# with open('dop_dataGPS.json', 'r') as f:
#     data = json.load(f)
#     gps_data = data[1]
#     f.close()
# with open('dop_dataGPSGal.json', 'r') as f:
#     data = json.load(f)
#     gpsGalileo_data = data[1]
#     f.close()
# with open('dop_dataGPSGalBei.json', 'r') as f:
#     data = json.load(f)
#     gpsGalileoBeidou_data = data[1]
#     f.close()
# with open('dop_dataGPSGalGlon.json', 'r') as f:
#     data = json.load(f)
#     gpsGalieoGlonass_data = data[1]
#     f.close()

# x_labels = np.linspace(0, 22600, 227)

#plt.plot(x_labels, all_data, label='All GNSS', color='#d62728')        # Soft blå1f77b4
#plt.plot(x_labels, gps_data, label='GPS', color='#ff7f0e')             # Oransje
#plt.plot(x_labels, gpsGalileo_data, label='GPS + Galileo', color='#2ca02c')  # Myk grønn
#plt.plot(x_labels, gpsGalileoBeidou_data, label='GPS + Galileo + BeiDou', color='#1f77b4') # Dempet rød
#plt.plot(x_labels, gpsGalieoGlonass_data, label='GPS + Galileo + GLONASS', color='#9467bd') # Lilla

# plt.gca().set_facecolor('#faf9f6')   # Bakgrunn inni selve plot-området
# plt.gcf().set_facecolor('#faf9f6')   # Bakgrunn utenfor plot-området (hele figuren)
# plt.xticks(rotation=45)
# plt.title('PDOP values along the road segment when using constellations', fontsize = 20)
# plt.xlabel('Distance along the road (m)', fontsize = 18)
# plt.ylabel('PDOP value', fontsize = 18)
# plt.ylim(0, max(gps_data)+1)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# konfigurasjoner = ["All", "GPS, Galileo, GLONASS", "GPS, Galileo, BeiDou", "GPS, Galileo", "GPS"]
# pdop_216 = [0.826, 1.008, 0.966, 1.302, 2.052]
# pdop_127 = [1.121, 1.378, 1.731, 12.532, 0]
# pdop_142 = [2.818, 4.805, 2.997, 5.537, 6.314]

# # --- 2. LAG STOLPEDIAAGRAM ---
# plt.figure(figsize=(10, 6))
# bars = plt.bar(konfigurasjoner, pdop_127, color='green', edgecolor='black')

# # --- 3. LEGG TIL VERDIMERKING PÅ TOPPEN ---
# for bar, val in zip(bars, pdop_127):
#     if val == 0:
#         # Legg til verdien på toppen av stolpen
#         plt.text(bar.get_x() + bar.get_width()/2, val + 0.05, f'None', ha='center', va='bottom', fontsize=16)
#     else:
#         plt.text(bar.get_x() + bar.get_width()/2, val + 0.05, f'{val:.3f}', ha='center', va='bottom',fontsize=16)

# # --- 4. FORMATERING ---
# plt.title("PDOP for Point 127 with Different GNSS Configurations", fontsize=18)
# plt.ylabel("PDOP Value", fontsize=18)
# plt.xticks(rotation=30, ha='right', fontsize=16)
# plt.ylim(0, max(pdop_127) + 1)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()

# # --- 5. VIS ---
# plt.show()

# plt.figure(figsize=(8, 5))
# plt.boxplot([df_127[df_127["Konfigurasjon"] == k]["PDOP"] for k in df_127["Konfigurasjon"]], labels=df_127["Konfigurasjon"])
# plt.title("PDOP for Point 127 with Different GNSS Configurations")
# plt.ylabel("PDOP Value")
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.tight_layout()
# plt.show()


#sammenligne med og uten terreng
PDOP_w = []
PDOP_wout = []
pointLat_list = []
pointLon_list = []

# with open('PDOP_wTerrain.json', 'r') as f:
#     data = json.load(f)
#     onluDop = []
#     for i in data:
#         onluDop.append(i[0][1])
#     PDOP_w = onluDop
#     f.close()
# with open('PDOP_wOutTerrain.json', 'r') as f:
#     data = json.load(f)
#     onluDop = []
#     for i in data:
#         onluDop.append(i[0][1])
#     PDOP_wout = onluDop
#     f.close()

with open('PDOPWTerrainDTM100m.json', 'r') as f:
    data = json.load(f)
    PDOP_w = data
    f.close()
with open('PDOPwithoutTerrain100m.json', 'r') as f:
    data = json.load(f)
    PDOP_wout = data
    f.close()
# with open('points100.json', 'r') as f:
#     data = json.load(f)
    
#     for point in data:
#         pointLon_list.append(point[0])
#         pointLat_list.append(point[1])
#     f.close()


x_labels = np.linspace(0, 48000, len(PDOP_w))
diff = []
for i in range(len(PDOP_w)):
    diff.append(PDOP_w[i] - PDOP_wout[i])


# # plt.plot(x_labels, PDOP_w, label='With Terrain Obstruction', color='#1f77b4')        # Soft blå
# # plt.plot(x_labels, PDOP_wout, label='Without Terrain Obstruction', color='#ff7f0e')             # Oransje
plt.plot(x_labels, diff, label='Difference in DOP', color='#ff1493')  # Myk grønn

plt.gca().set_facecolor('#faf9f6')   # Bakgrunn inni selve plot-området
plt.gcf().set_facecolor('#faf9f6')   # Bakgrunn utenfor plot-området (hele figuren)
plt.xticks(rotation=45)
plt.title('PDOP Differences With and Without Terrain Model Integration', fontsize=20)
plt.xlabel('Distance along the road (m)',fontsize=18)
plt.ylabel('PDOP value', fontsize=18)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#sammenligne  sør og nord
# PDOP_sør = []
# PDOP_nord = []
# pointSN_lat = []
# pointSN_lon = []

# with open('pdopSør_ny.json', 'r') as f:
#     data = json.load(f)
#     PDOP_sør = data
#     f.close()
# with open('pdopNord_ny.json', 'r') as f:
#     data = json.load(f)
#     PDOP_nord = data
#     f.close()
# # with open('pointsSouthNorth.json', 'r') as f:
# #     data = json.load(f)
# #     for point in data[0]:
# #         pointSN_lon.append(point[0])
# #         pointSN_lat.append(point[1])
# #     f.close()

# x_labels = np.linspace(0, 7100, 72)

# plt.plot(x_labels, PDOP_nord[:72], label='Northern Norway', color='#d62728')        # Soft blå
# plt.plot(x_labels, PDOP_sør[:72], label='Southern Norway ', color='#9467bd')             # Oransje

# plt.gca().set_facecolor('#faf9f6')   # Bakgrunn inni selve plot-området
# plt.gcf().set_facecolor('#faf9f6')   # Bakgrunn utenfor plot-området (hele figuren)
# plt.xticks(rotation=45)
# plt.title('PDOP Values in South vs North Norway', fontsize = 20)
# plt.xlabel('Points along the road (m)', fontsize = 18)
# plt.ylabel('PDOP value', fontsize = 18)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

#sammenligne iløpet av døgnet
# p1 = []
# p2 = []
# p3 = []
# w1 = []
# w2= []
# w3= []
# w4= []

# with open('pdop33.json', 'r') as f:
#     data = json.load(f)
#     p1 = data[1][0]
#     p2 = data[1][1]
#     p3 = data[1][3]
#     f.close()
# with open('pdopVaries.json', 'r') as f:
#     data = json.load(f)
  
#     w4 = np.mean(data[2], axis=0)
#     # # p1 = np.mean(data[0], axis=0)
#     # # # p2 = data[1]
#     # # p3 = np.median(data[1], axis=0)
#     f.close()
# with open('pdopWeek2.json', 'r') as f:
#     data2 = json.load(f)
    
#     w1 = np.mean(data2[0], axis=0)
#     w2 = np.mean(data2[1], axis=0)
#     w3 = np.mean(data2[2], axis=0)
#     w4 = np.mean(data2[3], axis=0)
#     f.close()


# x_labels = np.linspace(0, 23, 24)
# # print(len(w1))
# # print(len(w2))
# # print(len(w3))
# # print(len(w4))

# plt.plot(x_labels, p1, label='Point 1', color='#1f77b4')   # Blå (moderne)
# plt.plot(x_labels, p2, label='Point 2', color='#ff7f0e')   # Oransje (myk)
# plt.plot(x_labels, p3, label='Point 3', color='#2ca02c')   # Grønn

# plt.plot(x_labels, w1, label='GPS Week 2360', color='#1f77b4')   # Blå
# plt.plot(x_labels, w2, label='GPS Week 2361', color='#ff7f0e')   # Oransje
# plt.plot(x_labels, w3, label='GPS Week 2362', color='#2ca02c')   # Grønn
# plt.plot(x_labels, w4, label='GPS Week 2363', color='#d62728')   # Rød

# plt.gca().set_facecolor('#faf9f6')   # Bakgrunn inni selve plot-området
# plt.gcf().set_facecolor('#faf9f6')   # Bakgrunn utenfor plot-området (hele figuren)
# plt.xticks(x_labels)  # 👈 VIKTIG: vis ALLE x-ticks!
# plt.xticks(rotation=45)
# plt.title('Mean PDOP Values Throught the Day Over 4 Different Weeks.', fontsize = 20)
# plt.xlabel('Time of Day (hours)',fontsize=18)
# plt.ylabel('PDOP value', fontsize=18)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# import rasterio

# with rasterio.open("data/dom10/landsdekkende/64m1_1_10m_z33.tif") as src:
#     bounds = src.bounds
#     print("Venstre:", bounds.left)
#     print("Høyre:", bounds.right)
#     print("Nedre:", bounds.bottom)
#     print("Øvre:", bounds.top)

#     width = bounds.right - bounds.left
#     height = bounds.top - bounds.bottom
#     print("Bredde (m):", width)
#     print("Høyde (m):", height)
#     print("Areal (km²):", (width * height) / 1e6)


#heatmap med kart

# import pandas as pd
# import folium
# import branca.colormap as cm

# # --- 1. LAST INN DATA ---
# # Eksempel på dummydata – bytt med dine verdier
# data = {
#     "lat": pointLat_list,
#     "lon": pointLon_list,
#     "pdop": PDOP_w,  # Bruker kun de første 72 verdiene for å matche lengden på lat/lon
# }
# df = pd.DataFrame(data)

# # --- 2. LAG KART OG FARGESKALA ---
# m = folium.Map(
#     location=[df["lat"].mean(), df["lon"].mean()],
#     zoom_start=12,
#     tiles="CartoDB positron"
# )

# # Fargeskala fra grønn (bra PDOP) til rød (dårlig PDOP)
# colormap = cm.LinearColormap(
#     colors=['green', 'yellow', 'red'],
#     vmin=0,
#     vmax=5,
#     caption='PDOP Value'
# )
# colormap.add_to(m)

# # --- 3. TEGN FARGEDE SEGMENTER ---
# for i in range(len(df)-1):
#     p1 = (df.loc[i, "lat"], df.loc[i, "lon"])
#     p2 = (df.loc[i+1, "lat"], df.loc[i+1, "lon"])
#     avg_pdop = (df.loc[i, "pdop"] + df.loc[i+1, "pdop"]) / 2
#     folium.PolyLine(
#         locations=[p1, p2],
#         color=colormap(avg_pdop),
#         weight=8,
#         opacity=0.8,
#         tooltip=f'PDOP: {avg_pdop:.2f}'
#     ).add_to(m)

# # --- 4. VIS KART ---
# m.save("pdop_WithTerrain_DTM.html")

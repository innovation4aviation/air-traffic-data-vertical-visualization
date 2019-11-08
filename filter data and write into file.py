# -*- coding: utf-8 -*-
"""
"""


from shapely.geometry import Point, Polygon, LineString
import re

#import data
#please fill the path with specific information when run the code
f = open('','r') 
inf = f.read()
f.close()

#divide data 
#regular expression may change according to different data files
#in this case, using ADS-B data in 2019/3/12-2019/3/14 to analyze air traffic in KZTL FIR
pattern1 = "\"_id\":"
pattern2 = "\"vehicleposlen\":0\}"
lengthend = len(pattern2)
positions = [i.start() for i in re.finditer(pattern1, inf)]
positione = [i.start() for i in re.finditer(pattern2, inf)]
for m in range(len(positione)):
    positione[m] = positione[m] + lengthend
    
#the coordinates of FIR shape
#fill the list with specific data
lat_point = []
lon_point = []

coords=[[0 for i in range(2)] for j in range(50)]
for k in range(50):
    coords[k][0]=lat_point[k]
    coords[k][1]=lon_point[k]
poly=Polygon(coords)

st = inf[positions[0]:positione[0]]       #the number can be randomly chosen as long as smaller than len(positione)
pt = "\"edt\":\d+"
edt = re.findall(pt, st)[0]               ##re.findall returns result in 'list' format
pdt = "\"edt_datetime\":\"\S+\"\,\"edt\B"
edtd = re.findall(pdt, st)[0]
edt = int(re.findall("\d+", edt)[0])      #convert recoreded time into countable format
edtdt = re.findall("\d+", edtd)
sedtd = ''
for i in range(len(edtdt)):                #len(etad) can also be used
    sedtd = sedtd + edtdt[i]
t_standard = edt-((((int(sedtd[6:8])-12)*24+int(sedtd[8:10]))*60+int(sedtd[10:12]))*60+int(sedtd[12:14]))         #2019-3-12-00:00:00 is taken as the standard to calculate time

#set two groups of data for classification: altitude(0-50000ft/ scale: 100ft) & time (03/12/0:00-03/14/24:00/ scale: 10min)
#each sublist denotes flight distribution in each time period
#each element in sublist equals to the number of flights at each FL
#the last element in each sublist represents the number of invalid altitude in each time period
num = [[0 for p in range(518)] for q in range(480)]      
invalid_altitude = 0                     #count the number of flights with invalid altitude data 


#extract data 
#time is used as an indicator
for n in range(len(positions)):
    onedata = inf[positions[n]:positione[n]]
    s_time = "\"times\":\[[\d+\,]+\]"
    s_altitude = "\"altitudes\":\[[(?:\d+\,|\-d+\,|null\,)]+\]\,"
    d_time = re.findall("\d+", re.findall(s_time,onedata)[0])
    d_altitude = re.findall("(?:\-\d+|\d+|null)", re.findall(s_altitude,onedata)[0])
    s_coordinate = "\,\"line\":\{\"type\":\"LineString\"\,\"coordinates\":\S+\,\"times"
    coords= re.findall(s_coordinate,onedata)
    c_time = re.findall("\[(?:|(?:\d+|\-\d+)\.\d+|(?:\d+|\-\d+)),(?:(?:\d+|\-\d+)\.\d+|(?:\d+|\-\d+))\]", coords[0])
    if len(d_time) != len(d_altitude):
        print('error')
        exit
    else:
        if d_altitude == ['null']*len(d_altitude):
            invalid_altitude = invalid_altitude+1
            continue
        else:
             for j in range(len(c_time)):
                 lonlat= re.findall("(?:(?:\d+|\-\d+)\.\d+|(?:\d+|\-\d+))", c_time[j])
                 p1=float(lonlat[1])
                 p2=float(lonlat[0])
                 p=Point(p1, p2)
                 if p.within(poly):                                             #determine whether a point in inside the FIR or not
                     stime = (int(d_time[j])-t_standard)//600
                     if d_altitude[j] != 'null':
                         d_altitude[j] = int(d_altitude[j])
                         altitude = d_altitude[j]//100
                         num[stime][altitude+1] = num[stime][altitude+1]+1
                     else:
                         num[stime][517] = num[stime][517]+1


#write data filtering result into files-please use specific file path when run the code
f = open('','w')
f.write(str(num))
f.close()
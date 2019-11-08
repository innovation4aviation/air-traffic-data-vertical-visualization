# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 23:15:41 2019

@author: Jia
"""

from shapely.geometry import Point, Polygon, LineString
import re

#import data
#fill with specific file path
f = open('','r')
inf = f.read()
f.close()

#extract data 
#regular expression may vary according to different data files
pattern1 = "\"_id\":"
pattern2 = "\"vehicleposlen\":0\}"
lengthend = len(pattern2)
positions = [i.start() for i in re.finditer(pattern1, inf)]
positione = [i.start() for i in re.finditer(pattern2, inf)]
for m in range(len(positione)):
    positione[m] = positione[m] + lengthend

#fill with the coordinates of FIR shape
lat_point = []
lon_point = []
coords=[[0 for i in range(2)] for j in range(len(lat_point))]
for k in range(len(lat_point)):
    coords[k][0]=lat_point[k]
    coords[k][1]=lon_point[k]
poly=Polygon(coords)

#pick out the overflights
data=''
for n in range(len(positions)):
    onedata = inf[positions[n]:positione[n]]
    s_coordinate = "\,\"line\":\{\"type\":\"LineString\"\,\"coordinates\":\S+\,\"times"
    coords= re.findall(s_coordinate,onedata)
    c_time = re.findall("\[(?:|(?:\d+|\-\d+)\.\d+|(?:\d+|\-\d+)),(?:(?:\d+|\-\d+)\.\d+|(?:\d+|\-\d+))\]", coords[0])
    lonlat1=re.findall("(?:(?:\d+|\-\d+)\.\d+|(?:\d+|\-\d+))", c_time[0])
    lonlat2=re.findall("(?:(?:\d+|\-\d+)\.\d+|(?:\d+|\-\d+))", c_time[-1])
    p11=float(lonlat1[1])
    p12=float(lonlat1[0])
    p21=float(lonlat2[1])
    p22=float(lonlat2[0])
    p1=Point(p11, p12)
    p2=Point(p21, p22)
    if (not p1.within(poly)) and (not p2.within(poly)):
        data=data+onedata

#write flight information of overflights into the file
f = open('','w')
f.write(data)
f.close()
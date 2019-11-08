# -*- coding: utf-8 -*-
"""
"""

import re
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
import pandas as pd

#open the result file of 'filter data and write into file'
#please fill with specific file path information
f = open('','r')
inf = f.read()
f.close()

#extract data
pattern1 = "\["
pattern2 = "\]"
positions = [i.start() for i in re.finditer(pattern1, inf)]
positione = [i.start() for i in re.finditer(pattern2, inf)]

num=[]
for i in range(len(positions)-1):
    st = inf[positions[i+1]:positione[i]]
    s_num=re.findall("\d+",st)
    d_num=[int(j) for j in s_num]
    num.append(d_num)


labelx=pd.date_range("2019-03-13", "2019-03-14", freq="2H")    
##set 'time' as the x axis and shorten time duration to 24 hours
#only consider the altitude information in range[0ft, 50000ft] and 'null' data
num_0313 = [[0 for p in range(145)] for q in range(502)]
mmax = 0
for j in range(145):
    for k in range(502):
        num_0313[k][j]=num[144+j][k+1]
        if mmax < num_0313[k][j]:
            mmax = num_0313[k][j]
        num_0313[501][j]=num[144+j][517]
            
t_num=[0 for l in range(145)]
invalid_num=[0 for l in range(145)]
for m in range(145):
    for n in range(500):
        t_num[m]=t_num[m]+num_0313[n][m]
    invalid_num[m] = num_0313[501][m]
length = len(t_num)
fig, ax = plt.subplots(figsize=(40, 25))
ax.bar(x=range(length), height=t_num, width=0.6, color='lightsteelblue', label = 'valid data')
ax.bar(x=range(length), height=invalid_num, bottom=t_num, width=0.6, color='steelblue', label = 'invalid data')  
ax.set_xlim([-2,145])
ax.set_ylim([0,7000])
ax.set_xticks([0,12,24,36,48,60,72,84,96,108,120,132,144])
ax.set_yticks([0,1000,2000,3000,4000,5000,6000,7000])
ax.set_xticklabels(labelx, rotation=15, fontsize=15)
ax.set_yticklabels([0,1000,2000,3000,4000,5000,6000,7000], fontsize=15)
ax.set_xlabel(xlabel='Time (UTC)', size=25)
ax.set_ylabel(ylabel='Number', size=25)
ax.set_title("Number of flights", size=30)
plt.legend(loc='best', fontsize=20)
plt.show()
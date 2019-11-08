# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 18:34:38 2019

@author: Jia
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
    
#set 'time' as the x axis and shorten time duration to 24 hours
#only consider the altitude information in range[0ft, 50000ft] and 'null' data
num_0313 = [[0 for p in range(145)] for q in range(501)]
mmax = 0
for j in range(145):
    for k in range(501):
        num_0313[k][j]=num[144+j][k+1]
        if mmax < num_0313[k][j]:
            mmax = num_0313[k][j]
print('mmax = ', mmax)                 #max flight number at specific FL during 10min

#set the low & high for the number of flights
low, high=map(int,input("please enter the criteria of low and high traffic: ").split())

num_array = np.array(num_0313)         #format conversion

labelx=pd.date_range("13 3 2019", "14 3 2019", freq="2H")

fig=plt.figure(figsize=(40,28))
gs = gridspec.GridSpec(2, 3, width_ratios=[0.5, 14, 0.35], height_ratios=[10, 0.6])

ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax5 = plt.subplot(gs[4])


#draw the heatmap
#set the scale for axes and colorbar
cbar_kws = { 'ticks' : np.arange(0,400,40)}    
scale_interval = [' ']
cmap = sns.cubehelix_palette(100, start = 2.65, rot = 0, dark = 0, light = .98)     #set the color
sns.heatmap(num_array, vmin=0, vmax=360, cmap=cmap, cbar_kws=cbar_kws, cbar_ax=ax3, xticklabels = 12, yticklabels = 50, ax=ax2).invert_yaxis()
ax2.set_xticklabels(labelx, rotation=15, fontsize=12)
ax2.set_yticklabels(['FL0','FL50','FL100','FL150','FL200','FL250','FL300','FL350','FL400','FL450','FL500'], rotation=360, fontsize=15)
ax3.tick_params(labelsize=15)


#flight numbers along the time
t_num=[0 for i in range(145)]
for m in range(145):
    for n in range(501):
        t_num[m]=t_num[m]+num_0313[n][m]   
#horizontal bar showing detailed flight information at specific time point
tbar = [[0 for i in range(145)] for j in range(2)]
for j in range(2):
    for i in range(145):
        tbar[j][i] = t_num[i]
tbar_array = np.array(tbar)
cbar_kws = { 'ticks' : np.arange(0,7000,500) }    
scale_interval = [' ']
cmap = sns.cubehelix_palette(650, start = 2.92, rot = 0, dark = 0.2, light = .95) 
sns.heatmap(tbar_array, vmin=0, vmax=6500, cmap=cmap, cbar=False, cbar_kws = dict(use_gridspec=False,fraction=0.35,pad=0.2,location="bottom"), xticklabels=False, yticklabels=False, ax=ax5).invert_yaxis()
colorbar_ax5 = plt.gcf().axes[-1]
colorbar_ax5.tick_params(labelsize=15)

#flight numbers at specific FL 
h_num = [0 for i in range(501)]    
for p in range(501):
    for q in range(145):
        h_num[p] = h_num[p]+num_0313[p][q]
#vertical bar showing detailed flight information at specific flight level
hbar = [[0 for i in range(2)] for j in range(501)]
for i in range(2):
    for j in range(501):
        hbar[j][i] = h_num[j]
hbar_array = np.array(hbar)

cbar_kws = { 'ticks' : np.arange(0,19000,1000) }    
scale_interval = [' ']
cmap = sns.cubehelix_palette(1800, start = 2.25, rot = 0.05, dark = 0.25, light = .98)     #set the color
sns.heatmap(hbar_array, vmin=0, vmax=18000, cmap=cmap, cbar=False, cbar_kws = dict(use_gridspec=False,fraction=0.25,pad=0.5,location="left"), xticklabels=False, yticklabels=False,ax=ax1).invert_yaxis()
colorbar_ax1 = plt.gcf().axes[-1]
colorbar_ax1.tick_params(labelsize=15)

plt.tight_layout(pad=3.0, h_pad=5.3)
plt.suptitle('Number of Flights at each FL/Time', size=35)

#click to show detailed graphs
timenum=[[0 for p in range(145)] for q in range(501)]
timenum=num_0313
fnum=[[0 for p in range(51)] for q in range(145)]
for i in range(145):
    for j in range(50):
        for k in range(10):
            fnum[i][j]=fnum[i][j]+num_0313[j*10+k][i]
    fnum[i][50]=num_0313[500][i]  
labelt=pd.date_range("2019-03-13", "2019-03-14", freq="10T")
dates=pd.date_range("13 3 2019", "14 3 2019", freq="10T")
datex=pd.date_range("13 3 2019", "14 3 2019", freq="3H")
click1=0
click2=0

def onclick(event):
    subax = event.inaxes
    global click1
    global click2
    global annotation
    global ax7

    if event.xdata:
        if subax == ax2:            
            x=int(event.xdata//1)
            y=int(event.ydata//1)
            #use different colors to show the number of flights
            if num_0313[y][x]<=low:
                color="green"
            else:
                if num_0313[y][x] <= high:
                    color="gold"
                else:
                    color="orangered"
            if click2==0:
                annotation=ax2.annotate(labelt[x].to_pydatetime().strftime('%m-%d %H:%M')+'\nFL'+str(y)+'\n'+str(num_0313[y][x])+' flights', xy=(x+0.1, y+0.1), xycoords='data', xytext=(x-1, y+4),
                                       textcoords='data', size=14, horizontalalignment="left", arrowprops=None,
                                       bbox=dict(boxstyle="round", facecolor=color,edgecolor="0.5", alpha=0.3))
                plt.draw()
                click2 = click2+1
            else:
                annotation.remove()
                plt.draw()
                annotation=ax2.annotate(labelt[x].to_pydatetime().strftime('%m-%d %H:%M')+'\nFL'+str(y)+'\n'+str(num_0313[y][x])+' flights', xy=(x+0.1, y+0.1), xycoords='data', xytext=(x-1, y+4),
                                       textcoords='data', size=14, horizontalalignment="left", arrowprops=None,
                                       bbox=dict(boxstyle="round", facecolor=color,edgecolor="0.5", alpha=0.3))
                plt.draw()  
        else:                        
            if click1==0:
                left, bottom, width, height = 0.15, 0.25, 0.55, 0.55
                ax7 = fig.add_axes([left, bottom, width, height])
                ax7.patch.set_facecolor('snow')
                ax7.patch.set_alpha(0.9)
                if subax == ax1:
                    tdata = int(event.ydata//1)        
                    data=pd.DataFrame(timenum[tdata],dates)
                    sns.set(style="whitegrid")
                    sns.lineplot(data=data,linewidth=2,ci=None,legend=None,ax=ax7)
                    ax7.set_xticklabels(datex, rotation=15, fontsize=12, backgroundcolor='snow')
                    ax7.set_ylim([0,320])
                    ax7.set_yticks([0,40,80,120,160,200,240,280,320])
                    ax7.set_yticklabels([0,40,80,120,160,200,240,280,320], fontsize=15, backgroundcolor='snow')
                    ax7.set_ylabel('Number of Flights', size=18, backgroundcolor='snow')
                    plottitle='FL'+str(tdata)
                    ax7.text(x=0.9,y=0.95,s=plottitle,transform=ax7.transAxes,fontsize=20,bbox={'facecolor':'ivory', 'alpha':0.5, 'pad':5})
                    plt.draw()
                elif subax == ax5:
                    fdata = int(event.xdata//1)
                    ax7.barh(range(len(fnum[fdata])), fnum[fdata], color='lightsteelblue')
                    ax7.set_xlim([0, 450])
                    ax7.set_xticks([0,50,100,150,200,250,300,350,400,450])
                    ax7.set_xticklabels([0,50,100,150,200,250,300,350,400,450],fontsize=15, backgroundcolor='snow')
                    ax7.set_ylim([-5,50])
                    ax7.set_yticks([0,5,10,15,20,25,30,35,40,45,50])
                    ax7.set_yticklabels([0,50,100,150,200,250,300,350,400,450,500], fontsize=15, backgroundcolor='snow')
                    ax7.set_xlabel("Number of Flights", size=20, backgroundcolor='snow')
                    ax7.set_ylabel('Flight Level(FL)', size=20, backgroundcolor='snow')
                    datetimet = labelt[fdata].to_pydatetime()                                  
                    plottitle=datetimet.strftime('%Y-%m-%d %H:%M:%S')                              
                    ax7.text(x=0.8,y=0.95,s=plottitle,transform=ax7.transAxes,fontsize=20,bbox={'facecolor':'ivory', 'alpha':0.5, 'pad':5})
                    plt.draw()
                click1 =click1+1
            else:
                ax7.cla()
                plt.draw()
                if subax == ax1:
                    tdata = int(event.ydata//1)        
                    data=pd.DataFrame(timenum[tdata],dates)
                    sns.set(style="whitegrid")
                    sns.lineplot(data=data,linewidth=2,ci=None,legend=None,ax=ax7)
                    ax7.set_xticklabels(datex, rotation=15, fontsize=12, backgroundcolor='snow')
                    ax7.set_ylim([0,320])
                    ax7.set_yticks([0,40,80,120,160,200,240,280,320])
                    ax7.set_yticklabels([0,40,80,120,160,200,240,280,320], fontsize=15, backgroundcolor='snow')
                    ax7.set_ylabel('Number of Flights', size=18, backgroundcolor='snow')
                    plottitle='FL'+str(tdata)
                    ax7.text(x=0.9,y=0.95,s=plottitle,transform=ax7.transAxes,fontsize=20,bbox={'facecolor':'ivory', 'alpha':0.5, 'pad':5})
                    plt.draw()
                elif subax == ax5:
                    fdata = int(event.xdata//1)
                    ax7.barh(range(len(fnum[fdata])), fnum[fdata], color='lightsteelblue')
                    ax7.set_xlim([0, 450])
                    ax7.set_xticks([0,50,100,150,200,250,300,350,400,450])
                    ax7.set_xticklabels([0,50,100,150,200,250,300,350,400,450],fontsize=15, backgroundcolor='snow')
                    ax7.set_ylim([-5,50])
                    ax7.set_yticks([0,5,10,15,20,25,30,35,40,45,50])
                    ax7.set_yticklabels([0,50,100,150,200,250,300,350,400,450,500], fontsize=15, backgroundcolor='snow')
                    ax7.set_xlabel("Number of Flights", size=20, backgroundcolor='snow')
                    ax7.set_ylabel('Flight Level(FL)', size=20, backgroundcolor='snow')
                    datetimet = labelt[fdata].to_pydatetime()                                  
                    plottitle=datetimet.strftime('%Y-%m-%d %H:%M:%S')                               
                    ax7.text(x=0.8,y=0.95,s=plottitle,transform=ax7.transAxes,fontsize=20,bbox={'facecolor':'ivory', 'alpha':0.5, 'pad':5})
                    plt.draw()   
    else:
        if click1==1:
            ax7.remove()
            plt.draw()
            click1=0
        if click2==1:
            annotation.remove()
            plt.draw()
            click2=0   
cid = fig.canvas.mpl_connect('button_press_event', onclick)

    




"""
Created on Mon Jul 15 17:45:22 2019

@author: imon
"""
###########################################################
##################### IMAN KAHBASI ########################
##################################### IIEES ###############
import matplotlib.pyplot as plt
import numpy as np

print('enter command "help2me()" if you need it')
def help2me():
    print(
            '''
    this code has 3 simple function for read V1 file
    (file.V1 is strong motion or acceleration data of earthquake station)
    
        1)read_v1
            >>> path = 'path-of-file/namefile'
            
            # then
            >>> st = read_v1(path,method = 'obspystream')
            # or
            >>> data = read_v1(path,method = 'ascii')
            # or
            >>> data,st = read_v1(path,method = 'both')

           
            
            # data has all 3 component
            # data = [[comp1, time1, acc1],[comp2, time2, acc2],[comp3, time3, acc3]]
        
        2)v1_write_2column_file
            >>> v1_write_2column_file(data)
            # write 3 files with name of "input_file_name+component" in current directory 
    
        3)plot_v1
            >>> plot_v1(asciis)
            # save image 'output.png' in current directory
            
        send me any file.V1 that makes error
            '''
            )
def _read_component(iput,method):
    acc=[]
    for ii in range(0,6):
        line = iput.readline().split()
        if len(line)==2 and line[-1] == 'STATION':
            station = line[0]
            
    line = iput.readline().split() #line 7
    comp = line[1]
    if comp == '1' or comp == '2' or comp == '3':
        comp = 'L'+comp
        
    for ii in range(7,10):
        line = iput.readline()
    line = iput.readline().split() #line 11
    
    if len(line) == 8:
        duration = float(line[7])
        points = int(line[4])
        dt = duration/points
    
    for ii in range(11,27):
        line = iput.readline()
    while True:
        line = iput.readline()
        if line in ['/&\n','/&\r\n']:
            break
        
        l = int(len(line)/13)
        for ii in range(l):
            num = line[13*ii:13*(ii+1)].strip()
            num = float(num)
            acc.append(num)
            
    duration = dt * len(acc)
    time = list(np.arange(0,duration,dt))
    if method == 'obspystream' or method == 'both':
        from obspy.core.trace import Trace
        trace = Trace(data=np.array(acc))
        trace.stats.sampling_rate = 1/dt
        trace.stats.channel = comp
        if 'station' in locals():
            trace.stats.station = station
    if method == 'obspystream': 
        return trace
    if method == 'ascii':
        return [comp, time, acc]
    if method == 'both':
        return [comp, time, acc],trace
        

def read_v1(path_of_file,method = 'ascii'):
    global name2save
    name2save = path_of_file.split('.')[-2]
    File = open(path_of_file)
    if method == 'obspystream':
        from obspy.core.stream import Stream
        st = Stream()
        for ii in [1,2,3]:
            tr = _read_component(File,method)
            st += tr
        return st
            
    if method == 'ascii':
        asciis = []
        for ii in [1,2,3]:
            asciis.append(_read_component(File,method))
        return asciis
    
    if method == 'both': 
        asciis = []
        from obspy.core.stream import Stream
        st = Stream()
        for ii in [1,2,3]:
            asci,tr = _read_component(File,method)
            asciis.append(asci)
            st += tr
        return asciis,st

def v1_write_2column_file(asciis):
    for tr in asciis:
        amp = tr[2]
        time = tr[1]
        comp = tr[0]
        file = open(name2save+comp+'.txt','w')
        for ii in range(len(amp)):
            file.write(str(time[ii])+'\t\t'+str(amp[ii])+'\n')
        file.close()

def plot_v1(asciis):
    comp1,t1,a1 = asciis[0]
    
    comp2,t2,a2 = asciis[1]
    
    comp3,t3,a3 = asciis[2]
    
    fontsize = 30
    name_file = 'output'
    f = plt.figure(figsize=(30,30),dpi=100)
    plt.subplots_adjust(hspace=0.5)
    f.suptitle(name_file,fontsize=40,fontweight='black')
    f.add_subplot(311).plot(t1, a1, color='black',lw=0.9)
    plt.xlabel('time',fontsize=fontsize,fontweight='black')
    plt.ylabel('amplitude',fontsize=fontsize,fontweight='black')
    plt.title('component: '+comp1,loc='right', fontweight='black',fontsize=fontsize)
    plt.tick_params(labelsize=fontsize)
    
    f.add_subplot(312).plot(t2, a2, color='black',lw=0.9)
    plt.xlabel('time',fontsize=fontsize,fontweight='black')
    plt.ylabel('amplitude',fontsize=fontsize,fontweight='black')
    plt.title('component: '+comp2,loc='right', fontweight='black',fontsize=fontsize)
    plt.tick_params(labelsize=fontsize)
    
    f.add_subplot(313).plot(t3, a3, color='black',lw=0.9)
    plt.xlabel('time',fontsize=fontsize,fontweight='black')
    plt.ylabel('amplitude',fontsize=30,fontweight='black')
    plt.title('component: '+comp3,loc='right', fontweight='black',fontsize=fontsize)
    plt.tick_params(labelsize=fontsize)
    
    f.savefig(name_file+'.png',fontsize=fontsize,fontweight='black',dpi=120)
    
from math import cos,sin
from numpy import matmul
def rotate_xy(x, y, theta):
    new_x = []
    new_y = []

    R = [[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]

    if len(x) < len(y):
        y = y[:len(x)]
    elif len(x)>len(y):
        x = x[:len(y)]
    length = len(x)
    for ii in range(length):
        b = [ x[ii] , y[ii] ]
        amp = matmul(R, b)
        new_x.append(amp[0])
        new_y.append(amp[1])
    return new_x, new_y

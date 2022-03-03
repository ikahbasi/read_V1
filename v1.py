"""
Created on Mon Jul 15 17:45:22 2019

@author: IMAN KAHBASI form IIEES
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from math import cos, sin
from numpy import matmul


def _read_component(iput, method):
    acc = []
    for ii in range(0, 6):
        line = iput.readline().split()
        if len(line) == 2 and line[-1] == 'STATION':
            station = line[0]

    line = iput.readline().split()  # line 7
    comp = line[1]
    if comp == '1' or comp == '2' or comp == '3':
        comp = 'L'+comp

    for ii in range(7, 0):
        line = iput.readline()
    line = iput.readline().split()  # line 11
    dt = 0.05
    if len(line) == 8:
        duration = float(line[7])
        points = int(line[4])
        dt = duration/points

    for ii in range(11, 27):
        line = iput.readline()
    while True:
        line = iput.readline()
        if line in ['/&\n', '/&\r\n']:
            break

        _l = int(len(line)/13)
        for ii in range(_l):
            num = line[13*ii:13*(ii+1)].strip()
            num = float(num)
            acc.append(num)

    duration = dt * len(acc)
    time = list(np.arange(0, duration, dt))
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
        return [comp, time, acc], trace


def read_v1(path_of_file, method='ascii'):
    global name2save
    name2save = path_of_file.split('.')[-2]
    File = open(path_of_file)
    if method == 'obspystream':
        from obspy.core.stream import Stream
        st = Stream()
        for ii in [1, 2, 3]:
            tr = _read_component(File, method)
            st += tr
        return st

    if method == 'ascii':
        asciis = []
        for ii in [1, 2, 3]:
            asciis.append(_read_component(File, method))
        return asciis

    if method == 'both':
        asciis = []
        from obspy.core.stream import Stream
        st = Stream()
        for ii in [1, 2, 3]:
            asci, tr = _read_component(File, method)
            asciis.append(asci)
            st += tr
        return asciis, st


def v1_write_2column_file(asciis):
    for tr in asciis:
        amp = tr[2]
        time = tr[1]
        comp = tr[0]
        file = open(name2save+comp+'.txt', 'w')
        for ii in range(len(amp)):
            file.write(str(time[ii])+'\t\t'+str(amp[ii])+'\n')
        file.close()


def v1_write_4column_file(asciis, path2save, file2save):
    if not os.path.isdir('./output/'+path2save):
        os.makedirs('./output/'+path2save)
#    if os.path.isfile('./output/'+ file2save):
    file = open('./output/'+file2save+'.txt', 'w')
    for ii in range(len(asciis[0][2])):
        time = str(asciis[0][1][ii])
        l = str(asciis[0][2][ii])
        v = str(asciis[1][2][ii])
        t = str(asciis[2][2][ii])

        file.write(time+'\t'+l+'\t'+v+'\t'+t+'\n')
    file.close()


def plot_v1(asciis):
    comp1, t1, a1 = asciis[0]
    comp2, t2, a2 = asciis[1]
    comp3, t3, a3 = asciis[2]

    fontsize = 30
    name_file = 'output'
    f = plt.figure(figsize=(30, 30), dpi=100)
    plt.subplots_adjust(hspace=0.5)
    f.suptitle(name_file, fontsize=40, fontweight='black')
    f.add_subplot(311).plot(t1, a1, color='black', lw=0.9)
    plt.xlabel('time', fontsize=fontsize, fontweight='black')
    plt.ylabel('amplitude', fontsize=fontsize, fontweight='black')
    plt.title('component: '+comp1, loc='right', fontweight='black',
              fontsize=fontsize)
    plt.tick_params(labelsize=fontsize)

    f.add_subplot(312).plot(t2, a2, color='black', lw=0.9)
    plt.xlabel('time', fontsize=fontsize, fontweight='black')
    plt.ylabel('amplitude', fontsize=fontsize, fontweight='black')
    plt.title('component: '+comp2, loc='right', fontweight='black',
              fontsize=fontsize)
    plt.tick_params(labelsize=fontsize)

    f.add_subplot(313).plot(t3, a3, color='black', lw=0.9)
    plt.xlabel('time', fontsize=fontsize, fontweight='black')
    plt.ylabel('amplitude', fontsize=30, fontweight='black')
    plt.title('component: '+comp3, loc='right', fontweight='black',
              fontsize=fontsize)
    plt.tick_params(labelsize=fontsize)

    f.savefig(name_file+'.png', fontsize=fontsize,
              fontweight='black', dpi=120)


def rotate_xy(x, y, theta):
    new_x = []
    new_y = []

    R = [[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]

    if len(x) < len(y):
        y = y[:len(x)]
    elif len(x) > len(y):
        x = x[:len(y)]
    length = len(x)
    for ii in range(length):
        b = [x[ii], y[ii]]
        amp = matmul(R, b)
        new_x.append(amp[0])
        new_y.append(amp[1])
    return new_x, new_y


def makes_many(path):
    try:
        files = []
        paths = []
    #    path = '/media/imon/imon/DAtaEq/'
        for r, d, f in os.walk(path):
            for file in f:
                if file.split('.')[-1] == 'V1':
                    files.append(os.path.join(r, file))
                    paths.append(r)
        for f, p in zip(files, paths):
            data = read_v1(f)
            v1_write_4column_file(data, p, file2save=f)
    except Exception as error:
        print(error)
        print(p)
        globals().update(locals())
        raise

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from array import array
from math import sqrt
from ROOT import gROOT, TCanvas, TGraph2D

gROOT.SetStyle("Plain")

def create_graph(path, n):
    t = [map(float,line.split()) for line in open(path+'/temp.dat','r')]
    
    x, y, z = array('d'), array('d'), array('d')
    for i in range(n):
        name = '%s/%.2d.dat' % (path, i)
        print name
        data = [map(float, line.split()) for line in open(name)]
        
        ti = t[i][0]
        dti = (t[i][1]-t[i][0]) / len(data)
        
        for d in data:
            x.append(d[0])
            z.append(d[1])
            y.append(ti)
            ti += dti

    g = TGraph2D(len(x), x, y, z)
    g.SetTitle(';Magnetfeldstärke;Temperatur;Intensität')
    g.SetMarkerStyle(6)

    return g

ca = TCanvas('ca', 'Hanle-Signal, 90° Messung')
ga = create_graph('90', 37)
ga.Draw('P')
ca.Update()

cb = TCanvas('cb', 'Hanle-Signal, 0° Messung')
gb = create_graph('0', 35)
gb.Draw('P')
cb.Update()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
gROOT.SetStyle("Plain")


# constants
c = 299792458 # m/s
n = 1.000292 # brechzahl luft bodennah

#functions
#mittelwert, fehler
def mw(data):
    print data
    retval = [0,0]
    try:
        sum, squaresum = 0.0, 0.0
        for value in data:
            print 'Trying Value %s ...'%(value)
            sum += float(value)
            print 'converted.'
        count = len(data)
        print count
        print '%f  %f'%(sum, squaresum)
        r = sum/count
        print 'ok'        
        sr = sqrt(squaresum/(count*(count-1)))
        print r
        retval = [r, sr]
    except ValueError:
        print "Error while converting data!"
    return retval     
        
# data
freqs = []
times = []
for line in open('../data/eichung_frequenz.dat','r'):
    freqs.append(float(line.split()[0]))
    times.append(float(line.split()[1]))
count = len(times)

# fit and draw
g = TGraphErrors(count, array('d',times) ,array('d',freqs),array('d',[0.75]*count),
                 array('d',[0,0001]*count))
g.SetTitle(';time;frequency')
g.SetMarkerStyle(1)
g.SetMarkerColor(2)
g.SetMarkerSize(3.0)
f = TF1('Eichgerade', '[0]*x')
f.SetMarkerColor(3)
f.SetParameter(0, 1)
g.Fit(f, 'M')
c = TCanvas('Eichung', 'eichung')
c.SetGrid()
g.Draw('AP')
c.Update()

# Calculate Free Spectral Range of Resonator
delta_6 = 7.44 #us
delta_15 = 19.4
delta_3 = 3.72

delta = mw([delta_6/6, delta_15/15, delta_3/3])
print "Mittelwert für deltaFSR: %.4f +- %.4f  (%.4f per cent)"%(float(delta[0]),
                                                         float(delta[1]),
                                                         float(delta[1])/float(delta[0])) 
print "\nDone. Press any Key to continue ..."
raw_input();
print "bye"
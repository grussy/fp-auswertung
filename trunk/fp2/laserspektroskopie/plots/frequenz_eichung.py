#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin, sqrt
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

def gew_mittel(x, sx):
    assert len(x) == len(sx)
    suma = sumb = 0.
    for i in range(len(x)):
        suma += x[i] / sx[i]**2
        sumb += 1. / sx[i]**2
    return (suma/sumb, 1/sqrt(sumb))

As = []
sAs = []

# data
freqs = []
times = []
print "Dataset 0"
for line in open('../daten/eichung_frequenz_0.dat','r'):
    if (not line.strip()) or (line.strip()[0] == '#'): continue
    freqs.append(float(line.split()[0]))
    times.append(float(line.split()[1])*2)
count = len(times)
# fit and draw
g0 = TGraphErrors(count, array('d',times) ,array('d',freqs),array('d',[0.5]*count),
                 array('d',[0.5]*count))
g0.SetTitle(';time;frequency')
g0.SetMarkerStyle(1)
g0.SetMarkerColor(2)
g0.SetMarkerSize(3.0)
f0 = TF1('Eichgerade', '[0]*x')
f0.SetMarkerColor(3)
f0.SetParameter(0, 1)
g0.Fit(f0, 'MQ')
c0 = TCanvas('Eichung', 'eichung')
c0.SetGrid()
g0.Draw('AP')
c0.Update()
a, sa = f0.GetParameter(0), f0.GetParError(0)
As.append(a)
sAs.append(sa)
print "Frequency = A * Times[s] when A [s^-2] is\t%.3g +- %.3g\t(%.2f)"%(a, sa, (sa/a)*100)
raw_input();
# data
freqs = []
times = []
print "Dataset 0"
for line in open('../daten/eichung_frequenz_1.dat','r'):
    if (not line.strip()) or (line.strip()[0] == '#'): continue
    freqs.append(float(line.split()[0]))
    times.append(float(line.split()[1]))
count = len(times)
# fit and draw
g1 = TGraphErrors(count, array('d',times) ,array('d',freqs),array('d',[0.75]*count),
                 array('d',[0,0001]*count))
g1.SetTitle(';time;frequency')
g1.SetMarkerStyle(1)
g1.SetMarkerColor(2)
g1.SetMarkerSize(3.0)
f1 = TF1('Eichgerade', '[0]*x')
f1.SetMarkerColor(3)
f1.SetParameter(0, 1)
g1.Fit(f1, 'MQ')
c1 = TCanvas('Eichung', 'eichung')
c1.SetGrid()
g1.Draw('AP')
c1.Update()
a, sa = f1.GetParameter(0), f1.GetParError(0)
As.append(a)
sAs.append(sa)
print "Frequency = A * Times[s] when A [s^-2] is\t%.3g +- %.3g\t(%.2f)"%(a, sa, (sa/a)*100)
raw_input();
# data
freqs = []
times = []
print "Dataset 0"
for line in open('../daten/eichung_frequenz_2.dat','r'):
    if (not line.strip()) or (line.strip()[0] == '#'): continue
    freqs.append(float(line.split()[0]))
    times.append(float(line.split()[1]))
count = len(times)
# fit and draw
g2 = TGraphErrors(count, array('d',times) ,array('d',freqs),array('d',[0.75]*count),
                 array('d',[0,0001]*count))
g2.SetTitle(';time;frequency')
g2.SetMarkerStyle(1)
g2.SetMarkerColor(2)
g2.SetMarkerSize(3.0)
f2 = TF1('Eichgerade', '[0]*x')
f2.SetMarkerColor(3)
f2.SetParameter(0, 1)
g2.Fit(f2, 'MQ')
c2 = TCanvas('Eichung', 'eichung')
c2.SetGrid()
g2.Draw('AP')
c2.Update()
a, sa = f2.GetParameter(0), f2.GetParError(0)
As.append(a)
sAs.append(sa)
print "Frequency = A * Times[s] when A [s^-2] is\t%.3g +- %.3g\t(%.2f)"%(a, sa, (sa/a)*100)
raw_input();
# data
freqs = []
times = []
print "Dataset 0"
for line in open('../daten/eichung_frequenz_3.dat','r'):
    if (not line.strip()) or (line.strip()[0] == '#'): continue
    freqs.append(float(line.split()[0]))
    times.append(float(line.split()[1]))
count = len(times)
# fit and draw
g1 = TGraphErrors(count, array('d',times) ,array('d',freqs),array('d',[0.75]*count),
                 array('d',[0,0001]*count))
g1.SetTitle(';time;frequency')
g1.SetMarkerStyle(1)
g1.SetMarkerColor(2)
g1.SetMarkerSize(3.0)
f1 = TF1('Eichgerade', '[0]*x')
f1.SetMarkerColor(3)
f1.SetParameter(0, 1)
g1.Fit(f1, 'MQ')
c1 = TCanvas('Eichung', 'eichung')
c1.SetGrid()
g1.Draw('AP')
c1.Update()
a, sa = f1.GetParameter(0), f1.GetParError(0)
As.append(a)
sAs.append(sa)
print "Frequency = A * Times[s] when A [s^-2] is\t%.3g +- %.3g\t(%.2f)"%(a, sa, (sa/a)*100)

mitl, smitl = gew_mittel(As, sAs)
print "gew Mittel =\t%.3g +- %.3g\t(%.2f)"%(mitl, smitl, (smitl/mitl)*100)
print "\nDone. Press any Key to continue ..."
raw_input();
print "bye"
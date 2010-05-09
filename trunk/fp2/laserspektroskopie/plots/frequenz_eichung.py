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
##    print data
    retval = [0,0]
    try:
        sum, squaresum = 0.0, 0.0
        for value in data:
##            print 'Trying Value %s ...'%(value)
            sum += float(value)
##            print 'converted.'
        count = len(data)
##        print count
##        print '%f  %f'%(sum, squaresum)
        r = sum/count
##        print 'ok'        
        sr = sqrt(squaresum/(count*(count-1)))
##        print r
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
g0.SetTitle('Frequenzeichung;Zeit [us];Frequenz [Mhz]')
g0.SetMarkerStyle(3)
g0.SetMarkerColor(2)
g0.SetMarkerSize(1.5)
f0 = TF1('Eichgerade', '[0]*x')
f0.SetMarkerColor(3)
f0.SetParameter(0, 1)
g0.Fit(f0, 'MQ')
c0 = TCanvas('Eichung', 'eichung')
c0.SetGrid()
a, sa = f0.GetParameter(0), f0.GetParError(0)
ndf = f0.GetNDF()
chisq = f0.GetChisquare()
lg1 = TLegend(0.7, 0.8, 1, 1)
lg1.SetFillColor(0)
lg1.SetHeader('Linearer Fit A*x')
lg1.AddEntry(g0, 'Messdaten', 'p')
lg1.AddEntry(f0, 'A = %.2f +- %.2f (%.1f per cent)' % (a, sa , (sa/a)*100))
lg1.AddEntry(f0, '#chi^{2}/ndf = %.2f/%d = %.2f' % (chisq, ndf, chisq/ndf), 'p')
g0.Draw('AP')
lg1.Draw()
c0.Update()
a, sa = f0.GetParameter(0), f0.GetParError(0)
As.append(a)
sAs.append(sa)
print "Frequency = A * Times[s] when A [s^-2] is\t%.3g +- %.3g\t(%.2f)"%(a, sa, (sa/a)*100)
raw_input();
print "bye"
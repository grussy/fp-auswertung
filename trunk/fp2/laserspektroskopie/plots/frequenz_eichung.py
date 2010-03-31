#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
gROOT.SetStyle("Plain")

#################################################
# Eichung der Zeitachse zur Frequenz.
#################################################
f = []
t =[]
for line in open('../daten/frequenz_eichung.dat','r'):
    if not line.strip() or line.strip()[0] == '#': continue
    t.append(float(line.split()[0]))
    f.append(float(line.split()[1]))
print f
print t

count = len(t)
sf = [0.0001 for i in range(count)]
st = [1.5 for i in range(count)]
g = TGraphErrors(count, array('d',f) ,array('d',t), 
            array('d',[1e-4]*count), array('d',[1.5]*count))
g.SetTitle('Frequenzeichung; t / us; f / MHz;')
c = TCanvas('Frequenz Eichung', 'Frequenzeichung')
c.SetGrid()
fit = TF1('Eichgerade', '[0]*x')
#fit.SetParameters(1,1)
fit.SetMarkerColor(2)
g.Fit(fit, 'EMQ')
a, sa = fit.GetParameter(0), fit.GetParError(0)
#b, sb = fit.GetParameter(1), fit.GetParError(1)
chisq = fit.GetChisquare()
g.Draw('A*')
c.Update()

print "Variable |    Wert     |     Fehler   |    prozent "
print "  a            %.4e    |      %.4e    |      %.4f  "%(a, sa, sa/a)
#print "  b            %.4e    |      %.4e    |      %.4f  "%(b, sb, sb/b)
print ""
print "Chisquare was  %.4f"%(chisq)

print "\nDone. Press Enter to continue ..."
raw_input();

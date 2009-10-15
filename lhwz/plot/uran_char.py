#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from array import array
from math import sqrt
from ROOT import gROOT, TCanvas, TGraphErrors, TF1, TLegend

gROOT.SetStyle("Plain")



# Lese Messdaten ein
i = 0
x, y = array('d'), array('d')
for line in open("data/char_uran.dat", 'r'):
	linenew = line.replace(',', '.')
	xl, yl = map(float, linenew.split())
	x.append(xl); y.append(yl)
count = len(x)

#lese Untergrund ein
ux, uy = array('d'), array('d')
for line in open("data/untergrund_uran.dat", 'r'):
	linenew = line.replace(',', '.')
	xl, yl = map(float, linenew.split())
	ux.append(xl); uy.append(yl)
count = len(ux)



# Messfehler --------------------------------------------------------
t = 50.  #Messzeit pro Spannung
# Fehler auf die Spannung vernachlaessigt
sx = [0]*count

# Fehler der Zaehlrate
sy = [sqrt(z/t) for z in y]

# Untergrundfehler --------------------------------------------------------
t = 100. #Messzeit pro Spannung
# Fehler auf die Spannung vernachlaessigt
sux = [0]*count

# Fehler der Zaehlrate
suy = [sqrt(z/t) for z in y]

#Messkorrektur durch Untergrundabzug---------------------------------------------------------
dU = 100. #Spannungsdifferenz zw. Messpunkten
offset = int((ux[0] - x[0])/dU)

for z in range(len(ux)):
	y[z+offset] -= uy[z]

#fehler auf korrigierte Messung
sny = [sqrt(z**2 + zz**2) for z,zz in zip(sy,suy)]

c = TCanvas('c', 'Uran')
c.SetGrid()
c.SetLogy()

g = TGraphErrors(count, x, y, array('d', sx), array('d', sny))
g.SetTitle('; Zaehlrohrspannung / V; Zaehlrate')
g.GetYaxis().CenterTitle()
g.SetMarkerColor(2)
g.SetMarkerStyle(21)
g.SetMarkerSize(0.8)
g.Draw('AP')
c.Update()

line = sys.stdin.readline()
     

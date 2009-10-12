#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
from array import array
from math import sqrt
from ROOT import gROOT, TCanvas, TGraphErrors, TF1, TLegend, TGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Vgl. der Druckformel mit dem Diagramm
# -------------------------------------------------------------------

# Umrechnung der Temperatur [°C] in Druck [Torr]
def druck_falsch(T):
    if T >= -30 and T < 3.: A = 8.86; B = 0; C = -3440.
    elif T >= 3. and T <= 25: A = 10.6724; B = -0.847; C = -3342.26
    T += 273  # Temperatur von Celsius nach Kelvin
    return 10**A * 10**(C/T) * T**B

def druck(T):
    return 10**(8.86 - 3440/(T+273))

T = -22
t, p, pf = array('d'), array('d'), array('d')
while T < 10:
    T += 0.1
    t.append(T)
    p.append(druck(T))
    pf.append(druck_falsch(T))

g = TGraph(len(t), p, t)
g.SetMarkerColor(4)  # Blau
g.SetMarkerStyle(6)

gf = TGraph(len(t), pf, t)
gf.SetMarkerColor(3) # Gruen
gf.SetMarkerStyle(7)


# Ablesewerte
tx = [-0.4*48, -0.4*40, -0.4*29.3, -0.4*25.5, 0.4*2, 0.4*12, 0.4*19, 0.4*25.5]
px = [   2e-5,    3e-5,      5e-5,      6e-5,  2e-4,   3e-4,   4e-4,     5e-4]

gx = TGraph(len(tx), array('d',px), array('d',tx))
gx.SetMarkerColor(2) # Rot
gx.SetMarkerStyle(3)
    
c = TCanvas('c', 'Umrechnung: Temperatur nach Druck')
c.SetGrid()
gf.Draw('AP')
gx.Draw('P')
g.Draw('P')
c.Update()
line = sys.stdin.readline()

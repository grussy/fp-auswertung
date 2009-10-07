#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from array import array
from math import sqrt, pi
from ROOT import gROOT, TCanvas, TGraph, TGraphErrors, TLegend

# ROOT verfuegt leider nur ueber die Besselfunktionen J0 und J1,
# deshalb wird hier die Jn Implementierung von SciPy verwendet.
from scipy.special import jn

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Vergleich der Messwerte mit der Raman-Nath-Theorie
# -------------------------------------------------------------------


# Die Messdaten -----------------------------------------------------

sa = 0.1           # Ablesefehler in V
I0 = 12.6          # 0.Intensitaetsmaximum, 0.Ordnung [V]
sI0 = 0.20         # Fehler von I0

# 0.Ordnung: (Spannung/V, Intensitaet/V, Fehler auf Intensität)
order0 = [ (  0,   12.6, 0.2 ),
           (  0.5, 13,   0.2 ),
           (  1,   12.8, 0.2 ),
           (  1.5, 12.4, 0.2 ),
           (  2,   11.8, 0.2 ),
           (  2.5, 11,   0.2 ),
           (  3,   9.8,  0.2 ),
           (  3.5, 9,    0.2 ),
           (  4,   7.8,  0.2 ),
           (  4.5, 6.7,  0.1 ),
           (  5,   5,    0.1 ),
           (  5.5, 3.8,  0.1 ),
           (  6,   3.3,  0.1 ),
           (  6.5, 2.96, 0.1 ),
           (  7,   2.08, 0.1 ),
           (  7.5, 1.5,  0.1 ),
           (  8,   1,    0.1 ),
           (  8.5, 0.7,  0.1 ),
           (  9,   0.54, 0.05 ),
           (  9.5, 0.46, 0.05 ) ]

# 1.Ordnung: (Spannung/V, Intensitaet/V, Fehler auf Intensität)
order1 = [ (  0,   0,   0.2 ),
           (  0.5, 0,   0.2 ),
           (  1,   0,   0.2 ),
           (  1.5, 1,   0.2 ),
           (  2,   1.4, 0.2 ),
           (  2.5, 2,   0.2 ),
           (  3,   2.8, 0.2 ),
           (  3.5, 3.2, 0.2 ),
           (  4,   3.6, 0.2 ),
           (  4.5, 3.9, 0.1 ),
           (  5,   4.4, 0.1 ),
           (  5.5, 4.1, 0.1 ),
           (  6,   3.85,0.1 ),
           (  6.5, 3.37,0.1 ),
           (  7,   3,   0.1 ),
           (  7.5, 2.5, 0.1 ),
           (  8,   1.9, 0.1 ),
           (  8.5, 1.44,0.1 ),
           (  9,   1.1, 0.05 ),
           (  9.5, 0.91,0.05 ) ]

# 2.Ordnung: (Spannung/V, Intensitaet/V, Fehler auf Intensität)
order2 = [ (  0,   0,    0.2 ),
           (  0.5, 0,    0.2 ),
           (  1,   0,    0.2 ),
           (  1.5, 0,    0.2 ),
           (  2,   0,    0.2 ),
           (  2.5, 0,    0.2 ),
           (  3,   0,    0.2 ),
           (  3.5, 0.43, 0.2 ),
           (  4,   0.63, 0.2 ),
           (  4.5, 0.73, 0.1 ),
           (  5,   1,    0.1 ),
           (  5.5, 1.13, 0.1 ),
           (  6,   1.2,  0.1 ),
           (  6.5, 1.13, 0.1 ),
           (  7,   1.2,  0.1 ),
           (  7.5, 1.1,  0.1 ),
           (  8,   0.98, 0.1 ),
           (  8.5, 0.92, 0.1 ),
           (  9,   0.9,  0.05 ),
           (  9.5, 0.8,  0.05 ) ]

# 3.Ordnung: (Spannung/V, Intensitaet/V, Fehler auf Intensität)
order3 = [ (  0,   0,    0.2 ),
           (  0.5, 0,    0.2 ),
           (  1,   0,    0.2 ),
           (  1.5, 0,    0.2 ),
           (  2,   0,    0.2 ),
           (  2.5, 0,    0.2 ),
           (  3,   0,    0.2 ),
           (  3.5, 0,    0.2 ),
           (  4,   0,    0.2 ),
           (  4.5, 0,    0.1 ),
           (  5,   0.13, 0.1 ),
           (  5.5, 0.17, 0.1 ),
           (  6,   0.2,  0.1 ),
           (  6.5, 0.25, 0.1 ),
           (  7,   0.29, 0.1 ),
           (  7.5, 0.37, 0.1 ),
           (  8,   0.36, 0.1 ),
           (  8.5, 0.4,  0.1 ),
           (  9,   0.42, 0.05 ),
           (  9.5, 0.43, 0.05 ) ]

# 4.Ordnung: (Spannung/V, Intensitaet/V, Fehler auf Intensität)
order4 = [ (  0,   0,    0.2 ),
           (  0.5, 0,    0.2 ),
           (  1,   0,    0.2 ),
           (  1.5, 0,    0.2 ),
           (  2,   0,    0.2 ),
           (  2.5, 0,    0.2 ),
           (  3,   0,    0.2 ),
           (  3.5, 0,    0.2 ),
           (  4,   0,    0.2 ),
           (  4.5, 0,    0.1 ),
           (  5,   0,    0.1 ),
           (  5.5, 0,    0.1 ),
           (  6,   0,    0.1 ),
           (  6.5, 0,    0.1 ),
           (  7,   0,    0.1 ),
           (  7.5, 0,    0.1 ),
           (  8,   0.08, 0.1 ),
           (  8.5, 0.1,  0.1 ),
           (  9,   0.14, 0.05 ),
           (  9.5, 0.16, 0.05 ) ]

orders = [order0, order1, order2, order3, order4]
ocount = len(orders)


# Berechnung der Mittelwerte und Fehler -----------------------------

g = []
U, sU, I, sI, count = [], [], [], [], []
for o in orders:
    counti = len(o)
    
    Ui = [z[0] for z in o]
    sUi = [0.2]*counti

    # Normierten Intensitäten und ihr Fehler
    Ii = [(z[1] / I0) for z in o]
    sIi = [Iii*sqrt((z[2]/(z[1]+1e-10))**2 + (sI0/I0)**2) for z, Iii in zip(o,Ii)]

    U += [Ui]
    I += [Ii]
    count += [counti]
    sU += [sUi]
    sI += [sIi]

    gi = TGraphErrors(counti, array('d',Ui), array('d',Ii),
                      array('d',sUi), array('d',sIi))
    gi.SetTitle(';Spannung U [V];'
                'Normierte Intensit#ddot{a}t I/I_{0}')
    gi.SetMarkerColor(2)
    gi.SetMarkerStyle(21)
    gi.SetMarkerSize(0.7)

    g += [gi]


# Ermittle Umrechnungsfaktor ----------------------------------------

# Plotte 0. und 1. Ordnung
c01 = TCanvas('c01', '0. und 1. Ordnung')
c01.SetGrid()

g0 = g[0].Clone()
g0.Draw('ACP')

g1 = g[1].Clone()
g1.SetMarkerColor(3)
g1.Draw('CP')

l01 = TLegend(0.7, 0.8, 0.88, 0.88)
l01.SetFillColor(0)
l01.AddEntry(g0, '0. Ordnung', 'pl')
l01.AddEntry(g1, '1. Ordnung', 'pl')
l01.Draw()

c01.Update()

xg0min = 6.0   # Erstes Minimum der 0.Ordnung
xj0min = 2.4048 # Erstes Minimum von J0

xg1max = 5.0   # Erstes Maximum der 1.Ordnung
xj1max = 1.8412 # Erstes Maximum von J1

# Umrechungsfaktor
#b = (xj0min/xg0min + xj1max/xg1max) / 2.
b = xj1max/xg1max
print 'Erstes Minimum der 0.Ordnung: %.1f' % xg0min
print 'Erstes Minimum von J0: %.4f' % xj0min
print 'Erstes Maximum der 1.Ordnung: %.1f' % xg1max
print 'Erstes Maximum von J1: %.4f' % xj1max
print 'Umrechnungsfaktor b: %f' % b

# Vergleiche Messkurven mit Besselfunktionen ------------------------

# Erstelle Graphen der Besselfunktionen
gt = []
for i in range(ocount):
    Iti = [(jn(i,z*b))**2 for z in U[i]]
    gti = TGraph(len(Iti), array('d', U[i]), array('d', Iti))
    gti.SetTitle(';Spannung U [V];'
                 'Normierte Intensit#ddot{a}t I/I_{0}')
    gti.SetMarkerColor(4)
    gti.SetMarkerStyle(25)
    gti.SetMarkerSize(0.7)
    gt += [gti]

# Plotte Besselfunktionen und Messungen der jeweiligen Ordnungen
c = [] # Liste fuer GUI Instanzen
ly = [ 0.8, 0.8, 0.8, 0.8, 0.8 ] # Y-Koordinatrn fuer Legenden
lx = [ 0.7, 0.7, 0.2, 0.2, 0.2]    # X-Koordinaten fuer die Legenden
for i in range(ocount):
    ci = TCanvas('c%d' % i, '%d. Ordnung' % i)
    ci.SetGrid()

    gt[i].Draw('ACP')
    g[i].Draw('CP')

    l = TLegend(lx[i], ly[i], lx[i]+0.18, ly[i]+0.08)
    l.SetFillColor(0)
    l.AddEntry(g[i], 'Messwerte', 'pl')
    l.AddEntry(gt[i], 'Theoretische Werte', 'pl')
    l.Draw()

    ci.Update()

    c += [(ci,l)]

line = sys.stdin.readline()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
from array import array
from math import sqrt, cos, pi
from ROOT import gROOT, TCanvas, TF1
from pickle import load

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Bestimmung der Aperturfunktion von Gitter 1
# -------------------------------------------------------------------

L = 6.328 * 1e-7  # Wellenlaenge des Lasers [m]

# Lade die in konst.py berechneten Werte der Gitterkonstanten
Ks = load(open('k.dat', 'r'))

# Gitterkonstante von Gitter 1 [m], Fehler [m]
K, sK = Ks[0]

# Messung der Intensitäten ------------------------------------------

# Die gemessenen Intensitäten [cm]: ( (I-, I+), [V/cm] )
#messI = [ ( ( 15.35, 15.35 ), 0.50 ),    # 0. Ordnung
#          ( (  6.90,  6.90 ), 0.05 ),    # 1. Ordnung
#          ( (  4.50,  4.15 ), 0.05 ),    # 2. Ordnung
#          ( (  2.84,  2.28 ), 0.05 ),    # 3. Ordnung
#          ( (  1.18,  1.22 ), 0.05 ),    # 4. Ordnung
#          ( (  0.31,  0.30 ), 0.05 ) ]   # 5. Ordnung


sIa = 0.1  # Ablesefehler [cm]

# Mittelwerte der Intensitäten [V]
#I = [(z[0][0] + z[0][1])/2 * z[1] for z in messI]

# Intensitäten in [mV]
I = [6585., 259., 180., 116., 58. ]

count = len(I)
# Fehler der Mittelwerte [mV]
#sI = [z[1]/sqrt(2) * sIa for z in messI]
sI = [100., 10., 10., 10., 5. ]

print 'Intensitäten:'
for i in range(count):
    print 'I%d = (%.5f +- %.5f)mV' % (i, I[i], sI[i])


# Erzeuge Aperturfunktion g -----------------------------------------

expr = 'sqrt([0])'
for i in range(1,count):
    expr += ' + sqrt([%d])*cos(x/[%d]*2*pi*%d)' % (i,count,i)

g = TF1('g', expr, -K/2, K/2)
g.SetParameters(array('d', I+[K]))
g.SetNpx(1000)


# Spaltbreite / Spaltabstand ----------------------------------------

# Bestimme Spaltbreite (volle Breite des halben Maximums, fwhm)
gmax, gmin = g.GetMaximum(), g.GetMinimum()
h = (gmax-gmin)/2 + gmin
fwhm = abs(g.GetX(h))*2
w, d, sd = fwhm, K-fwhm, sK

# Verhaeltnis und Fehler
v = w/d
sv = sd/d*v
print '\nSpaltbreite / Spaltabstand:'
print 'Spaltbreite w [m]: %e' % w
print 'Spaltabstand d [m]: %e +- %e' % (d,sd)
print 'Verhältnis w/d: %f +- %f' % (v,sv)


# Plot der Aperturfunktion ------------------------------------------

g.SetRange(-3*K/2, 3*K/2)
c = TCanvas('c', 'Aperturfunktion von Gitter 1')
c.SetGrid()
g.SetTitle('')
g.Draw()
c.Update()
line = sys.stdin.readline()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from math import sqrt
from pickle import load

# -------------------------------------------------------------------
# Bestimmung der maximalen Auflösungsvermögen der fünf Gitter
# -------------------------------------------------------------------

# Lade die in konst.py berechneten Werte der Gitterkonstanten
K = load(open('k.dat', 'r'))

d  = 3e-3    # Durchmesser des Laserstrahls [m]
sd = 0.5e-3  # Fehler [m]

# Maximale Ordnung
m = [ 5, 2, 1, 4, 3 ]

# Namen der vermessenen Gitter
names = [ '1', '3', '4', 'PHYWE08534', 'PHYWE08540' ]

for i, m, (Ki,sKi) in zip(range(len(K)), m, K):

    # Anzahl der Linien und deren Fehler
    N = d/Ki   
    sN = N * sqrt((sd/d)**2 + (sKi/Ki)**2)

    # Maximales Auflösungsvermögen und dess Fehler
    a = N * m
    sa = a * sqrt((sd/d)**2 + (sKi/Ki)**2)
    
    print '\nGitter %s:' % names[i]
    print 'N: %f +- %f' % (N, sN)
    print 'a: %f +- %f' % (a, sa)

#line = sys.stdin.readline()

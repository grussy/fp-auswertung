#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from konst import *
from messung import *
from math import sqrt
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Berechnung der Dipolmomente  der mit verschiedenen Gegenstaenden
# -------------------------------------------------------------------

# Abstand z [m], in schleife.py bestimmt
z, sz = (0.030922471837111904, 0.0026243745469483252)

# Abgeschaetzter Fehler der Spannungsdifferenz durch den Untergrund [V]
sUunt = 0.02

# Lade Messdaten
mg = lade_gegenstaende()
mgf = filter(lambda mi: mi.fitable, mg)

# Fuehre Fits durch
print 'Sinus-Fit'
for m in mg:
    if m.fitable:
        m.fit()
        print '%s: rchisq = %.5f, dU = %.4f +- %.4f' % (
            m.name, m.rchisq, m.dU, m.sdU)
    #m.draw()
    #m.vdraw()

# Berechne Dipolmomente und Magnetfelder
print '\nBerechnung der Dipolmomente und Magnetfelder'
for m in mgf:
    # Berechne Bz und seinen Fehler
    Bz = m.dU/(2 * m.si * Feff)
    sBz = Bz * (m.sdU+sUunt)/m.dU
    m.Bz, m.sBz = Bz, sBz

    # Berechne Dipolmoment
    pm = 2*pi * z**3 * Bz / mu0
    spm = pm * sqrt( (sBz/Bz)**2 + (3.*sz/z)**2 )
    m.pm, m.spm = pm, spm

    print '%s: Bz = %g +- %g (%.1f%%), pm = %g +- %g (%.1f%%)' % (
        m.name, Bz, sBz, sBz/Bz*100, pm, spm, spm/pm*100)


# Berechne Magnetfelder der Nicht-Dipole
print '\nBerechnung der Magnetfelder der Nicht-Dipole'
si = 10./phi0
sdU = 0.05
md = [('zyl_b.dat', 0.63), ('tina_1', 0.23), ('korken', 1.68), ('1cent', 1.23)]

for m in md:
    name, dU = m
    
    # Berechne Bz und seinen Fehler
    Bz = dU/(2 * si * Feff)
    sBz = Bz * (sdU+sUunt)/dU
    print '%s: Bz = %g +- %g (%.1f%%)' % (name, Bz, sBz, sBz/Bz*100)
    

# Erzeuge TeX Tabellen
#import texgen
#texgen.write_table_gegenstaende(mg)
#texgen.write_table_gegenstaende_fit(mg)

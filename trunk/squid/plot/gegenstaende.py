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
zm, szm = (0.044, 0.01)

# Abgeschaetzter Fehler der Spannungsdifferenz durch den Untergrund [V]
sUunt = 0.02

# Lade Messdaten
mgf = lade_gegenstaende()

# Fuehre Fits durch
print 'Sinus-Fit'
for m in mgf:
        m.fito()
        print '%s: rchisq = %.5f, dU = %.4f +- %.4f' % (
            m.name, m.rchisq, m.dU, m.sdU)
    	m.draw()
	m.vdraw()
zm, szm = (0.044, 0.01)
# Berechne Dipolmomente und Magnetfelder
print '\nBerechnung der Dipolmomente und Magnetfelder'
for m in mgf:
    # Berechne Bz und seinen Fehler
    Bz = (Ffl*m.dU)/m.si
    sBz = Bz * (m.sdU+sUunt)/m.dU
    m.Bz, m.sBz = Bz, sBz

    # Berechne Dipolmoment
    pm = 2*pi * zm**3 * Bz / mu0
    spm = pm * sqrt( (sBz/Bz)**2 + (3.*szm/zm)**2 )
    m.pm, m.spm = pm, spm

    print '%s: Bz = %g +- %g (%.1f%%), pm = %g +- %g (%.1f%%)' % (
        m.name, Bz, sBz, sBz/Bz*100, pm, spm, spm/pm*100)
    
print '\nfür unsere SimKarte mit wechselnder Amplitude muss wohl noch ein anderer Fit gemacht werden, \n hier wird auch das Dipolmoment nicht mehr stimmen da wir eine andere als nur eine einfache \n Sinusabhängikeit haben. Ansonsten finde ich auch hier keine Fehler mehr. '
raw_input();
# Erzeuge TeX Tabellen
#import texgen
#texgen.write_table_gegenstaende(mg)
#texgen.write_table_gegenstaende_fit(mg)

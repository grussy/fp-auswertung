#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from konst import *
from messung import *
from tools import gew_mittel, arith_mittel
from math import sqrt, pi
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Plotten und Fitten der Messungen mit Leiterschleife
# -------------------------------------------------------------------

# Lade Messdaten
msf = lade_schleife()
print '\nAus einem ersten Fit an R1...R4 wurde das gewichtete Mittel von omega zu %f +- %f bestimmt\n\n'%(omega,somega)
#msf = filter(lambda mi: mi.fitable, ms)

# Fuehre Fits durch -------------------------------------------------
print 'Sinus-Fits ohne Steigung:'
for m in msf:
        m.fito()
	print 'Funktion fuer %s: %f + %f sin(x + %f )'%(
		m.name,m.a,m.b,m.c)
        print 'rchisq = %.5f, dU = %.4f +- %.4f' % (
        	m.rchisq, m.dU, m.sdU)

print '\nSinus-Fits mit Steigung:'
for m in msf:
        m.fitm()
	print 'Funktion fuer %s: %f + %f x + %f sin(x + %f )'%(
		m.name,m.a,m.d,m.b,m.c)
        print 'rchisq = %.5f, dU = %.4f +- %.4f' % (
        	m.rchisq, m.dU, m.sdU)
	m.draw()
	m.vdraw()


# Berechne Magnetfeld Bz und die Hoehe z des SQUIDs -----------------
print '\nBerechnung von Bz und z'
z, sz = [], []
for m in msf:
    # Berechne Bz und seinen Fehler
    Bz = m.dU/(2 * m.si * Feff)
    sBz = Bz * m.sdU/m.dU
    m.Bz, m.sBz = Bz, sBz

    # Berechne z (der rel. Fehler von r**2 dominiert mit 20%)
    a = mu0 * m.Ibat/(2*Bz)
    zi = sqrt( (a*r**2)**(2./3.) - r**2 )
    szi = abs((2./3. * a * r / (a*r**2)**(1./3.) - r) / zi * sr)
    m.z, m.sz = zi, szi
    z += [zi]; sz += [szi]
    
    print '%s: Bz = %g +- %g (%.1f%%), z = %f +- %f (%.1f%%)' % (
        m.name, Bz, sBz, sBz/Bz*100, zi, szi, szi/zi*100)

# relativer systematischer Fehler von z
rzs = abs((1. - 1./3.*(a*r**2)**(2./3.) / ((a*r**2)**(2./3.) - r**2)) * sr/r)

# Berechne gewichtetes Mittel
zm, szm = gew_mittel(zip(z,sz))
szms = zm * rzs
print '\nGewichtetes Mittel von z: %f +- %f (stat) +- %f (syst)' % (
    zm, szm, szms)


# Berechne Magnetfeld Bz und die Hoehe z des SQUIDs -----------------
print '\nBerechnung der Dipolmomente'
for m in msf:
    # Berechne theoretischen Wert aus der Schleifenflaeche und dem Strom
    pt = m.Ibat * A
    spt = 2 * pi * r * m.Ibat * sr
    m.pt, m.spt = pt, spt

    # Bestimme Dipolmoment aus Bz und dem Abstand
    pm = 2*pi * zm**3 * m.Bz / mu0
    spm = pm * sqrt( (m.sBz/m.Bz)**2 + (3.*(szm+szms)/zm)**2 )
    m.pm, m.spm = pm, spm
    
    print '%s: pt = %g +- %g, pm = %g +- %g' % (
        m.name, pt, spt, pm, spm)
raw_input();

# Erzeuge TeX Tabellen
import texgen
#texgen.write_table_schleife(msf)
texgen.write_table_schleife_fit(msf)
texgen.write_table_z(msf)
texgen.write_table_schleife_dipol(msf)

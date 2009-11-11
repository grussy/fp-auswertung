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
print '\nAus einem ersten Fit an R1...R4 wurde das gewichtete Mittel von omega zu %f +- %f bestimmt'%(omega,somega)

# Fuehre Fits durch -------------------------------------------------
#print 'Sinus-Fits ohne Steigung:'
#for m in msf:
#        m.fito()
#	print 'Funktion fuer %s: %f + %f sin(x + %f )'%(
#		m.name,m.a,m.b,m.c)
#        print 'rchisq = %.5f, dU = %.4f +- %.4f' % (
#        	m.rchisq, m.dU, m.sdU)


print '\nSinus-Fits mit Steigung:'
for m in msf:
        m.fitm()
#	print 'Funktion fuer %s: %f + %f x + %f sin(x + %f )'%(
#		m.name,m.a,m.d,m.b,m.c)
        print 'rchisq = %.5f, dU = %.4f +- %.4f' % (
        	m.rchisq, m.dU, m.sdU)
#	m.draw()
#	m.vdraw()


# Berechne Magnetfeld Bz -----------------
print '\nBerechnung von Bz'
for m in msf:
    # Berechne Bz und seinen Fehler
    Bz = (m.dU*Ffl)/m.si
    sBz = Bz * m.sdU/m.dU
    m.Bz, m.sBz = Bz, sBz
    
    print '%s: Bz = (%f * Ffl)/%f = %g +- %g (%.1f%%)' % (
        m.bez,m.dU,m.si, Bz, sBz, sBz/Bz*100)


zm, szm = (0.044, 0.005)
print '\nAbstand Squid - Probe z: %f +- %f (%f%%)' % (
    zm, szm,float((szm/zm)*100))
print '\na, b:%g  %g'%(r_a, r_b_innen+d)
print '\nFläche der Schleife:%g +- %g'%(A, sA)
print '\nalte Fläche der Schleife:%g +- %g'%(A_alt, sA_alt)

# Berechne Dipolmomente -----------------
print '\nBerechnung der Dipolmomente'
for m in msf:
    # Berechne theoretischen Wert aus der Schleifenflaeche und dem Strom
    pt = m.Ibat * A
    spt = (sA/A)*pt
    m.pt, m.spt = pt, spt

    # Bestimme Dipolmoment aus Bz und dem Abstand
    pm = 2*pi * zm**3 * m.Bz / mu0
    spm = pm * sqrt( (m.sBz/m.Bz)**2 + (3.*(szm)/zm)**2 )
    #spm = m.sBz
    m.pm, m.spm = pm, spm
    
    print '%s & %.2g & %.2g & %.2g & %.2g & %.2g & %.2g & %.2f \\\\' % (
        m.bez, m.Bz, m.sBz, pm, spm, pt, spt, pt/pm)
   
print '\n --> Wie du siehst stimmen die Werte um den Faktor 1,6 nicht. Fehler viel zu gross. Finde aber keine Fehler im Code mehr'
raw_input();

# Erzeuge TeX Tabellen
import texgen
#texgen.write_table_schleife(msf)
#texgen.write_table_schleife_fit(msf)
#texgen.write_table_z(msf)
#texgen.write_table_schleife_dipol(msf)

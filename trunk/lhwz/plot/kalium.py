#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from ROOT import gROOT, TCanvas, TGraphErrors, TF1
from array import array
from math import sqrt, log

# -------------------------------------------------------------------
# Massenabhängige Zählrate bei Kalium
# -------------------------------------------------------------------

gROOT.SetStyle("Plain")
c = TCanvas('c', 'Massenabhängige Zählrate bei Kalium')
c.SetGrid()


# Messung -----------------------------------------------------------

t = 460.    # Messzeit
tu = 865.  # Messzeit fuer den Untergrund [s]
u = 0.925   # Untergrundrate [cps]

# Messwerte: (Masse mit Schälchen, Rate)
nm = [
    (2.9505, 4.917),
    (2.8464, 5.670),
    (2.7500, 5.639),
    (2.6524, 5.609),
    (2.5542, 5.143),
    (2.4520, 5.463),
    (2.3526, 5.237),
    (2.2565, 4.846),
    (2.1458, 4.900),
    (2.0495, 4.791)]

# Aufteilen in separate Listen
m = map(lambda z: z[0], nm)
n = map(lambda z: z[1], nm)

count = len(nm)               # Anzahl der Messungen

m0 = 1.795                   # Schälchenmasse
m = map(lambda mi: mi-m0, m)  # Korrigiere Massenwerte
n = map(lambda ni: ni-u, n)  # Korrigiere Rate

sm = [sqrt(2)/1000. for mi in m]          # Fehler der Massewerte
sn = [sqrt((ni+u)/t + u/tu) for ni in n]  # Fehler der Raten


# Aufteilen in zu fittende (1) und zu verwerfende (2) Messungen
m1 = [m[1],m[2],m[3],m[5],m[7],m[6]]
n1 = [n[1],n[2],n[3],n[5],n[7],n[6]]
sm1 = [sm[1],sm[2],sm[3],sm[5],sm[7],sm[6]]
sn1 = [sn[1],sn[2],sn[3],sn[5],sn[7],sn[6]]
count1 = len(m1)

m2 = [m[0],m[4],m[8],m[9]]
n2 = [n[0],n[4],n[8],n[9]]
sm2 = [sm[0],sm[4],sm[8],sm[9]]
sn2 = [sn[0],sn[4],sn[8],sn[9]]
count2 = len(m2)


# Plot --------------------------------------------------------------

g = TGraphErrors(count1, array('d',m1), array('d',n1),
                 array('d',sm1), array('d',sn1))
g.SetTitle('Kalium')
g.GetXaxis().SetTitle('Masse m [g]')
g.GetXaxis().SetLimits(0.2,1.2)
g.GetYaxis().SetTitle('Messrate n [1/s]')
g.SetMarkerColor(4)
g.SetMarkerStyle(21)
g.SetMarkerSize(0.8)
g.SetMinimum(1)
g.SetMaximum(6)
g.Draw('AP')
#c.Update()

# Extra-Graph für die nicht zu fittenden Messungen
g2 = TGraphErrors(count2, array('d',m2), array('d',n2),
                  array('d',sm2), array('d',sn2))
g2.SetMarkerColor(2)
g2.SetMarkerStyle(25)
g2.SetMarkerSize(0.8)
g2.Draw('P')
c.Update()

# Fit ---------------------------------------------------------------

# Kurvenanpassung
#i0 = 0
f = TF1('f', '[0]*(1-exp(-[1]*x))', 0, 1.2)#, 0, x[i0]+0.02)
#f = TF1('f', '[0]*x+[1]', 0, 2)
f.SetParameter(0, 0.001)
f.SetParameter(1, 0.5)
g.Fit(f, 'QR')

c.Update()

a = f.GetParameter(0)
sa = f.GetParError(0)
b = f.GetParameter(1)
sb = f.GetParError(1)

print "\nKurvenanpassung:"
print "a: %.4f +- %.4f" % (a,sa)
print "b: %.4f +- %.4f" % (b,sb)


# Spezifische Beta-Aktivität ----------------------------------------

fb = 1.29      # Rückstreufaktor
D = 2.*a*b/fb  # spez. Aktivität
sD = sqrt((sa/a)**2 + (sb/b)**2) * D  # Fehler der spez. Aktivität

print "\nSpezifische Beta-Aktivität:"
print "D: %f +- %f" % (D,sD)


# Halbwertszeit -----------------------------------------------------

na = 6.0221367 * 10**23  # Avogadrozahl

mr_k  = 39.10            # relative Atommase von K [g/mol]
mr_cl = 35.45            # relative Atommase von Cl [g/mol]
mr_kcl = mr_k + mr_cl

h_rel = 0.000118         # relative Häufigkeit von K-40 in KCl

t12_beta = log(2) * na * h_rel / (D * mr_kcl)
t12a_beta = t12_beta / 3600./24./365.
st12_beta = sD/D * t12_beta
st12a_beta = sD/D * t12a_beta

t12 = t12_beta / 1.13
st12 = sD/D * t12
t12a = t12 / 3600./24./365.
st12a = sD/D * t12a

print "\nHalbwertszeit:"
print "Beta-Halbwertszeit [s]: %g +- %g" % (t12_beta, st12_beta)
print "Beta-Halbwertszeit [a]: %g +- %g" % (t12a_beta, st12a_beta)
print "Halbwertszeit von K-40 [s]: %g +- %g" % (t12, st12)
print "Halbwertszeit von K-40 [a]: %g +- %g" % (t12a,st12a)
line = sys.stdin.readline()

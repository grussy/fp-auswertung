#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
from array import array
from math import sqrt
from ROOT import gROOT, TCanvas, TGraphErrors, TF1, TLegend

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Bestimmung der Schallwellenlaenge
# -------------------------------------------------------------------

L = 6.328e-7  # Wellenlaenge des Lasers [m]
sd = 1      # Ablesefehler vom oszi[us]

# Eichung der Zeitachse mit Gitter R --------------------------------

Kr = 1./80./100.  # Gitterkonstante von R [m]

# Gitter R: Abstand zur 0.Ordnung in us (-2..+2)
rd = [ -175.38, -87.63, 87.75, 175.5 ]
rm = [    -2,     -1,     1,      2 ]

rcount = len(rd)
srd = [sd]*rcount
#rt_pro_cm = 5e-5
rt = [z / 1000. /1000. for z in rd]  # Umrechnung von cm nach s
srt = [sd / 1000. / 1000.] * rcount   # Fehler auf die Zeit

# sin(theta) aus den Ordnungen und der Gitterkonstante berechnen
rsinth = [m * L / Kr for m in rm]

# beim Fit gibts Probleme, wenn hier 0 steht
srsinth = [1e-10] * rcount

# Plotte sin(theta) nach t
cr = TCanvas('cr', 'Eichung der Zeitachse')
cr.SetGrid()
gr = TGraphErrors(rcount, array('d',rt), array('d',rsinth),
                  array('d',srt), array('d',srsinth))
gr.SetTitle(';Zeit t [s];sin #theta')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')

# Linearer Fit
fr = TF1('fr', '[0]*x + [1]')
gr.Fit(fr, 'Q')
ar, sar = fr.GetParameter(0), fr.GetParError(0)
br, sbr = fr.GetParameter(1), fr.GetParError(1)

lr = TLegend(0.55, 0.14, 0.88, 0.34)
lr.SetFillColor(0)
lr.AddEntry(gr, 'Messdaten, Gitter R', 'p')
lr.AddEntry(fr, 'Linearer Fit: sin #theta = at + b', 'l')
lr.AddEntry(fr, 'a = %.4f #pm %.4f' % (ar,sar), '')
lr.AddEntry(fr, 'b = %.4g #pm %.4g' % (br,sbr), '')
lr.AddEntry(fr, '#chi^{2} = %.4g' % fr.GetChisquare(), '')
lr.Draw()
cr.Update()

print "Eichung, Gitter R:"
print 'sin(theta) = a * t + b'
print 'a: %.5f +- %.5f' % (ar, sar)
print 'b: %.5g +- %.5g' % (br, sbr)


# Bestimmung der Schallwellenlaenge ---------------------------------

# Abstand zur 0.Ordnung in us (-4..+3)
d = [-77.25, -57.45, -38.75, -19.85, 19.8, 38.95, 57.65]
m = [  -4,     -3,     -2,     -1,     1,    2,     3 ]

count = len(d)
#tpcm = 5e-5    # Zeit pro cm
sm = [0]*count # Kein Fehler auf die Beugungsorgnungen m

# Zeit und Fehler in s
t = [z / 1000. / 1000. for z in d]
st = sd /1000./1000.

# sin(theta) und Fehler anhand der Eichung berechnen
sinth = [ar*z+br for z in t]
ssinth = [sqrt((z*sar)**2 + (ar*st)**2 + sbr**2) for z in t]

# Plotte sin(theta) nach m
c = TCanvas('c', 'Phasengitter')
c.SetGrid()

g = TGraphErrors(count, array('d',m), array('d',sinth),
                 array('d',sm), array('d',ssinth))
g.SetTitle(';Beugungsordnung m;sin #theta')
g.GetYaxis().CenterTitle()
g.SetMarkerColor(2)
g.SetMarkerStyle(3)
g.Draw('AP')

# Linearer Fit
f = TF1('f', '[0]*x + [1]')
g.Fit(f, 'Q')
a, sa = f.GetParameter(0), f.GetParError(0)
b, sb = f.GetParameter(1), f.GetParError(1)

l = TLegend(0.55, 0.14, 0.88, 0.34)
l.SetFillColor(0)
l.AddEntry(g, 'Messdaten, Phasengitter', 'p')
l.AddEntry(f, 'Linearer Fit: sin #theta = am + b', 'l')
l.AddEntry(f, 'a = %.4g #pm %.4g' % (a,sa), '')
l.AddEntry(f, 'b = %.4g #pm %.4g' % (b,sb), '')
l.AddEntry(f, '#chi^{2} = %.4g' % f.GetChisquare(), '')
l.Draw()

c.Update()

Ls = L/a       # Schallwellenlaenge [m]
sLs = Ls*sa/a  # Fehler [m]

print '\nPhasengitter:'
print 'a: %.5e +- %.5e,' % (a,sa),
print 'b: %.5g +- %.5g' % (b,sb)
print 'Schallwellenlaenge Ls [m]: %.5e +- %.5e' % (Ls,sLs)

cs = 1111.       # Schallgeschwindigkeit in Isooktan [m/s]
nu = cs/Ls       # Ultraschallfrequenz [Hz]
snu = nu*sLs/Ls  # Fehler der Frequenz [Hz]

print 'Ultraschallfrequenz nu [MHz]: %f +- %f' % (nu/1e6, snu/1e6)
line = sys.stdin.readline()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from array import array
from math import sqrt
from pickle import dump
from ROOT import gROOT, TCanvas, TGraphErrors, TF1, TLegend

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Bestimmung der Gitterkonstanten der Amplitudengitter
# -------------------------------------------------------------------

L = 6.328e-7  # Wellenlaenge des Lasers [m]
sd = 0.3      # Ablesefehler Zeitachse [us]

# Eichung der Zeitachse mit Gitter R --------------------------------

Kr = 1./80./100.  # Gitterkonstante von R [m]

# Gitter R: Abstand zur 0.Ordnung in us (-4..+4)
rd = [ -324.25, -244.5, -163.8, -81.650, 81.650, 163.550, 243.875, 325.5 ]
rm = [  -4,       -3,      -2,     -1,      1,       2,      3,       4 ]
rcount = len(rd)

# Flehler der Zeitachse in s
srt = [sd / 1000. /1000. ]*rcount

#rt_pro_cm = 5e-5
rt = [z / 1000. / 1000. for z in rd]  # Umrechnung von us nach s
#srt = [sd * rt_pro_cm] * rcount   # Fehler auf die Zeit

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


# Gitterkonstanten von Gitter 1 bis 5 -------------------------------

# Gitter 1: Abstand zur 0.Ordnung in us (-4..+4)
d1 = [ -293.250, -222.5, -147.0, -75.25, 74.250, 148.5, 223.375, 299.5 ]
m1 = [   - 4,    -3,    -2,    -1,    1,    2,    3,    4 ]

# Gitter 3: Abstand zur 0.Ordnung in us (-2..+2)
d3 = [ -186.125, -92.375, 93.125, 186.875 ]
m3 = [    -2,    -1,    1,    2 ]

# Gitter 4: Abstand zur 0.Ordnung in us (-3..+3)
d4 = [ -287.750, -93.750, 93.5, 281.0]
m4 = [    -3,    -1,    1,    3 ]

# Gitter PHYWE08534: Abstand zur 0.Ordnung in us (-2..+2)
d08534 = [ -152.125, -76.0, 76.125, 151.5 ]
m08534 = [    -2,    -1,    1,    2 ]

# Gitter 5: Abstand zur 0.Ordnung in us (-2..+2)
d08540 = [ -376.0, -283.5, -191.0, -95.5, 94.25, 187.375, 286.0, 382.250 ]
m08540 = [  -4,   -3,    -2,    -1,    1,    2 ,   3,   4 ]

# Zeit pro cm fuer Gitter 1-5
#t_pro_cm = [5e-5, 1e-4, 5e-5, 1e-4, 1e-4]

d = [d1, d3, d4, d08534, d08540]
m = [m1, m3, m4, m08534, m08540]

# Listen c fuer GUI-Instanzen und K fuer die Gitterkonstanten
c, K = [], []

# Namensgebung der Gitter
names = [ '1', '3', '4', 'PHYWE08534', 'PHYWE08540' ]

# Fitte Gitter 1-5 und berechne die Gitterkonstanten K[i]
for i in range(len(d)):

    di = d[i]
    count = len(di)
    #tpcm = t_pro_cm[i]

    # Beugungsorgnungen m
    mi = m[i]
    smi = [0]*count

    # Zeit und Fehler in s
    ti = [z / 1000. / 1000. for z in di]
    sti = sd / 1000. / 1000.

    # sin(theta) und Fehler anhand der Eichung berechnen
    sinth = [ar*z+br for z in ti]
    ssinth = [sqrt((z*sar)**2 + (ar*sti)**2 + sbr**2) for z in ti]

    # Plotte sin(theta) nach m
    ci = TCanvas('c%d' % (i+1), 'Gitter %s' % names[i])
    ci.SetGrid()
    
    gi = TGraphErrors(count, array('d',mi), array('d',sinth),
                      array('d',smi), array('d',ssinth))
    gi.SetTitle('; Beugungsordnung m; sin #theta')
    gi.GetYaxis().CenterTitle()
    gi.SetMarkerColor(2)
    gi.SetMarkerStyle(3)
    gi.Draw('AP')

    # Linearer Fit
    fi = TF1('f%d' % (i+1), '[0]*x + [1]')
    gi.Fit(fi, 'Q')
    a, sa = fi.GetParameter(0), fi.GetParError(0)
    b, sb = fi.GetParameter(1), fi.GetParError(1)

    l = TLegend(0.55, 0.14, 0.88, 0.34)
    l.SetFillColor(0)
    l.AddEntry(gi, 'Messdaten, Gitter %s' % names[i], 'p')
    l.AddEntry(fi, 'Linearer Fit: sin #theta = am + b', 'l')
    l.AddEntry(fi, 'a = %.4g #pm %.4g' % (a,sa), '')
    l.AddEntry(fi, 'b = %.4g #pm %.4g' % (b,sb), '')
    l.AddEntry(fi, '#chi^{2} = %.4g' % fi.GetChisquare(), '')
    l.Draw()
    
    ci.Update()

    

    Ki = L/a       # Gitterkonstante [m]
    sKi = Ki*sa/a  # Fehler [m]

    print '\nGitter %s:' % names[i]
    print 'a: %.5e +- %.5e,' % (a,sa),
    print 'b: %.5g +- %.5g' % (b,sb)
    print 'K [m]: %.5e +- %.5e' % (Ki,sKi)

    # Referenzen sichern, damit sie nicht entsorgt werden
    c += [(ci,gi,fi,l)]

    # fuege Ki und sKi in die Liste K der Gitterkonstanten ein
    K += [(Ki,sKi)]

# Schreibe die ermittelten Gitterkonstanten K1..K5 zur weiteren
# Verwendung (aufloesung.py) in eine Datei
dump(K, open('k.dat', 'w'))
line = sys.stdin.readline()

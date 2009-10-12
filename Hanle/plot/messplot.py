#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from array import array
from ROOT import gROOT, TCanvas, TGraphErrors, TLegend

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Plotten der Messdaten
# -------------------------------------------------------------------

#messreihen = [('90', range(17, 57)), ('0', range(23, 57)), ('45', range(1,3))]
messreihen = [('45', range(1,3))]

temp, namen = [], []
for m in messreihen:
    for i in m[1]:
        namen += ['data/%sGRAD/%s.tab' % (m[0],i)]
        temp += [i]

anzahl = len(namen)

c, g, l = [], [], []
for i in range(anzahl):
    #name = '%s/%.2d.dat' % (messreihe,i)
    name = namen[i]
    t = (float(temp[i])-36.)*5./9.
    
    # Lese Messdaten ein
    z = 0
    time, y, x = array('d'), array('d'), array('d')
    for line in open(name, 'r'):
	    if z == 0:
 		z = 2
            else:
		linenew = line.replace(',', '.')
            	tl, yl, xl = map(float, linenew.split())
            	x.append(xl); y.append(yl); time.append(tl)
    sx = array('d', [0.00001]*len(x))
    sy = array('d', [0.001]*len(x))

    # Erzeuge Graphen aus den Messdaten
    gi = TGraphErrors(len(x), x ,y, sx, sy)
    gi.SetTitle(';Magnetfeldst#ddot{a}rke;Intensit#ddot{a}t')

    li = None
    if name[:2] == '90': li = TLegend(0.52, 0.14, 0.88, 0.29)
    else: li = TLegend(0.52, 0.73, 0.88, 0.88)
    li.SetFillColor(0)
    li.AddEntry(gi, 'Messreihe ' + name, 'l')
    li.AddEntry(gi, 'T = %.1f#circC' % t, '')


    # 4 Messkurven auf eine Seite
    if i%4 == 0:
        titel = 'messung_%.2d-%.2d' % (i,i+3)
        ci = TCanvas(titel, titel)
        #ci.Divide(2,2)
        c += [ci]

    ci.cd(i%4 + 1)
    gi.Draw('AP')
    li.Draw()
    ci.Update()

    g += [gi]; l += [li]
line = sys.stdin.readline()

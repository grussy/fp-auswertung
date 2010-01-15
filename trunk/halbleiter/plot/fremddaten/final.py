#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from math import pi, cos, sin, exp, sqrt
from array import array
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors

#List of Fit parameters [[59,5keV: amp, samp, mean, smean, sig, ssig],[122keV: ...],..]
Si, CdTe = [], []
#Constants[mm^2]
acdte, asi = 23, 100

x = []
y = []
i = 0
a = 0

for line in open("CdTe_AM.asc"):
	y += [float(line)]
	x += [i]
	i += 1
count = len(x)
raw_cdte_am_x, raw_cdte_am_y = x,y
# Erzeuge Graphen
g = TGraph(count, array('d',x) ,array('d',y))
g.SetTitle(';Kanal;Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(100, 350)
h = g.GetHistogram()
h.SetMinimum(0)
h.SetMaximum(200)


#fr = TF1('fr', '[0]*(1 / sqrt(2 * pi * [1]**2)) * exp(-((x-[2])**2)/(2 * [1]**2)))', 0, 200)
fr = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 280, 350)
fr.SetParameter(0, 200)
fr.SetParameter(1, 1)
fr.SetParameter(2, 300)
fr.SetNpx(1000)
g.Fit(fr, 'QR')
title = "test"
c = TCanvas('c_'+title, title)
c.SetGrid()
g.Draw('AP')
c.Update()

CdTe.append([fr.GetParameter(0), fr.GetParError(0), 
    fr.GetParameter(2), fr.GetParError(2), 
    fr.GetParameter(1), fr.GetParError(1)])

x = []
y = []
i = 0
a = 0

for line in open("CdTe_co57.asc"):
	y += [float(line)]
	x += [i]
	i += 1
count = len(x)
raw_cdte_co_x, raw_cdte_co_y = x,y
# Erzeuge Graphen
g = TGraph(count, array('d',x) ,array('d',y))
g.SetTitle(';Kanal;Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(600, 780)
##h = g.GetHistogram()
##h.SetMinimum(0)
##h.SetMaximum(200)

#fr = TF1('fr', '[0]*(1 / sqrt(2 * pi * [1]**2)) * exp(-((x-[2])**2)/(2 * [1]**2)))', 0, 200)
fr1 = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 645, 700)
fr1.SetParameters(300, 658, 20)
fr2 = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 720, 780)
fr2.SetParameters(300, 740, 20)
g.Fit(fr1, 'QR')
g.Fit(fr2, 'QR+')
title = "test"
c = TCanvas('c_'+title, title)
c.SetGrid()
g.Draw('AP')
c.Update()

CdTe.append([fr1.GetParameter(0), fr1.GetParError(0), 
    fr1.GetParameter(2), fr1.GetParError(2), 
    fr1.GetParameter(1), fr1.GetParError(1)])
    
CdTe.append([fr2.GetParameter(0), fr2.GetParError(0), 
    fr2.GetParameter(2), fr2.GetParError(2), 
    -fr2.GetParameter(1), fr2.GetParError(1)])

x = []
y = []
i = 0
a = 0

for line in open("Si_Am.mca"):
	y += [float(line)]
	x += [i]
	i += 1
count = len(x)
raw_si_am_x, raw_si_am_y = x,y
# Erzeuge Graphen
g = TGraph(count, array('d',x) ,array('d',y))
g.SetTitle(';Kanal;Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(250, 350)
h = g.GetHistogram()
h.SetMinimum(0)
h.SetMaximum(20)

#fr = TF1('fr', '[0]*(1 / sqrt(2 * pi * [1]**2)) * exp(-((x-[2])**2)/(2 * [1]**2)))', 0, 200)
fr = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 280, 350)
fr.SetParameter(0, 200)
fr.SetParameter(1, 1)
fr.SetParameter(2, 300)
fr.SetNpx(1000)
g.Fit(fr, 'QR')
title = "test"
c = TCanvas('c_'+title, title)
c.SetGrid()
g.Draw('AP')
c.Update()

x = []
y = []
i = 0

Si.append([fr.GetParameter(0), fr.GetParError(0), 
    fr.GetParameter(2), fr.GetParError(2), 
    fr.GetParameter(1), fr.GetParError(1)])

for line in open("Si_co57.asc"):
	y += [float(line)]
	x += [i]
	i += 1
count = len(x)
raw_si_co_x, raw_si_co_y = x,y
# Erzeuge Graphen
g = TGraph(count, array('d',x) ,array('d',y))
g.SetTitle(';Kanal;Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(550, 750)
h = g.GetHistogram()
h.SetMinimum(0)
h.SetMaximum(260)

#fr = TF1('fr', '[0]*(1 / sqrt(2 * pi * [1]**2)) * exp(-((x-[2])**2)/(2 * [1]**2)))', 0, 200)
fr1 = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 550, 670)
fr1.SetParameters(300, 620, 20)
fr2 = TF1('fr', '[0]*( 1 / sqrt(2 * pi * [1]^2) * exp(- 0.5 * (x - [2])^2 / [1]^2))', 650, 750)
fr2.SetParameters(300, 700, 20)
g.Fit(fr1, 'QR')
g.Fit(fr2, 'QR+')
title = "test"
c = TCanvas('c_'+title, title)
c.SetGrid()
g.Draw('AP')
c.Update()

Si.append([fr1.GetParameter(0), fr1.GetParError(0), 
    fr1.GetParameter(2), fr1.GetParError(2), 
    fr1.GetParameter(1), fr1.GetParError(1)])
    
Si.append([fr2.GetParameter(0), fr2.GetParError(0), 
    fr2.GetParameter(2), fr2.GetParError(2), 
    fr2.GetParameter(1), fr2.GetParError(1)])
    
print "\nData of CdTe Detector:"
print "\n Data of 59,5 keV Peak:"
print "  Hoehe: %.2f+-%.2f" % (CdTe[0][0], CdTe[0][1])
print "  Center: %.2f+-%.2f" % (CdTe[0][2], CdTe[0][3])
print "  Breite: %.2f+-%.2f" % (CdTe[0][4], CdTe[0][5])


print "\n Data of 122,06 keV Peak:"
print "  Hoehe: %.2f+-%.2f" % (CdTe[1][0], CdTe[1][1])
print "  Center: %.2f+-%.2f" % (CdTe[1][2], CdTe[1][3])
print "  Breite: %.2f+-%.2f" % (CdTe[1][4], CdTe[1][5])

print "\n Data of 136,47 keV Peak:"
print "  Hoehe: %.2f+-%.2f" % (CdTe[2][0], CdTe[2][1])
print "  Center: %.2f+-%.2f" % (CdTe[2][2], CdTe[2][3])
print "  Breite: %.2f+-%.2f" % (CdTe[2][4], CdTe[2][5])

print "\nData from Si Detector:"
print "\n Data of 59,5 keV Peak:"
print "  Hoehe: %.2f+-%.2f" % (Si[0][0], Si[0][1])
print "  Center: %.2f+-%.2f" % (Si[0][2], Si[0][3])
print "  Breite: %.2f+-%.2f" % (Si[0][4], Si[0][5])

print "\n Data of 122,06 keV Peak:"
print "  Hoehe: %.2f+-%.2f" % (Si[1][0], Si[1][1])
print "  Center: %.2f+-%.2f" % (Si[1][2], Si[1][3])
print "  Breite: %.2f+-%.2f" % (Si[1][4], Si[1][5])

print "\n Data of 136,47 keV Peak:"
print "  Hoehe: %.2f+-%.2f" % (Si[2][0], Si[2][1])
print "  Center: %.2f+-%.2f" % (Si[2][2], Si[2][3])
print "  Breite: %.2f+-%.2f" % (Si[2][4], Si[2][5])

# Energieskalierung: linearer fit
#datenarrays
chan_si, schan_si = [],[]
chan_cd, schan_cd = [],[]
# lade daten
for i in range(0,3):
    chan_si.append(float(Si[i][2]))
    schan_si.append(float(Si[i][3]))
    chan_cd.append(float(CdTe[i][2]))
    schan_cd.append(float(CdTe[i][3]))
e = [59.5, 122.06, 136.47]
count = len(e)
se = [1e-10 for i in range(count)]

# Erzeuge Graphen
mg = TMultiGraph()
mg.SetTitle(';Energie [keV];Kanal')

g = TGraphErrors(count, array('d',e), array('d',chan_si), array('d',se), array('d',schan_si))
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(20)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
##xa = g.GetXaxis()
##xa.SetLimits(550, 750)
##h = g.GetHistogram()
##h.SetMinimum(0)
##h.SetMaximum(260)
fr = TF1('fr', '[0]*x+[1]', 58, 140)
fr.SetParameters(5, 1)
g.Fit(fr, 'QR')
si_a, si_b = fr.GetParameter(0), fr.GetParameter(1)

g1 = TGraphErrors(count, array('d',e), array('d',chan_cd), array('d',se), array('d',schan_cd))
g1.GetHistogram().SetTitleOffset(1.3, 'Y')
g1.SetMarkerStyle(22)
g1.SetMarkerColor(4)
g1.SetMarkerSize(1.0)
##xa = g.GetXaxis()
##xa.SetLimits(550, 750)
##h = g.GetHistogram()
##h.SetMinimum(0)
##h.SetMaximum(260)
fr1 = TF1('fr', '[0]*x+[1]', 58, 140)
fr1.SetParameters(5, 1)
g1.Fit(fr1, 'QR')
cdte_a, cdte_b = fr.GetParameter(0), fr.GetParameter(1)

aLegend = TLegend(0.75,0.4,0.9,0.5)
aLegend.AddEntry(g, "Si","p")
aLegend.AddEntry(g1, "CdTe","p")


title = "Energieeichung"
c = TCanvas('c_'+title, title)
c.SetGrid()
mg.Add(g)
mg.Add(g1)
mg.Draw('AP+')
aLegend.Draw('AP')
c.Update()

print "\nCalculating..."
rel_59 = (Si[0][2]*acdte)/(CdTe[0][2]*asi)
srel_59 = rel_59*sqrt((Si[0][3]/Si[0][2])**2+(CdTe[0][3]/CdTe[0][2])**2)
rel_122 = (Si[1][2]*acdte)/(CdTe[1][2]*asi)
srel_122 = rel_59*sqrt((Si[1][3]/Si[1][2])**2+(CdTe[1][3]/CdTe[1][2])**2)
rel_136 = (Si[2][2]*acdte)/(CdTe[2][2]*asi)
srel_136 = rel_59*sqrt((Si[2][3]/Si[2][2])**2+(CdTe[2][3]/CdTe[2][2])**2)

rer_59_si = (2.35*Si[0][4])/Si[0][2]
srer_59_si = rer_59_si*sqrt((Si[0][3]/Si[0][2])**2+(Si[0][5]/Si[0][4])**2)
rer_122_si = (2.35*Si[1][4])/Si[1][2]
srer_122_si = rer_59_si*sqrt((Si[1][3]/Si[1][2])**2+(Si[1][5]/Si[1][4])**2)
rer_136_si = (2.35*Si[2][4])/Si[2][2]
srer_136_si = rer_59_si*sqrt((Si[2][3]/Si[2][2])**2+(Si[2][5]/Si[2][4])**2)

rer_59_cdte = (2.35*CdTe[0][4])/CdTe[0][2]
srer_59_cdte = rer_59_cdte*sqrt((CdTe[0][3]/CdTe[0][2])**2+(CdTe[0][5]/CdTe[0][4])**2)
rer_122_cdte = (2.35*CdTe[1][4])/CdTe[1][2]
srer_122_cdte = rer_59_cdte*sqrt((CdTe[1][3]/CdTe[1][2])**2+(CdTe[1][5]/CdTe[1][4])**2)
rer_136_cdte = (2.35*CdTe[2][4])/CdTe[2][2]
srer_136_cdte = rer_59_cdte*sqrt((CdTe[2][3]/CdTe[2][2])**2+(CdTe[2][5]/CdTe[2][4])**2)
print "\nAbsobtionsverhaeltnisse:"
print '\nA bei 59keV: %f'%rel_59
print 'A bei 122keV: %f'%rel_122
print 'A bei 136keV: %f'%rel_136

#tex:
print '%.2f & %.2f & %.2f \\\\'%(1.4, rel_59*100, srel_59*100)
print '%.2f & %.2f & %.2f \\\\'%(1.83, rel_122*100, srel_122*100)
print '%.2f & %.2f & %.2f \\\\'%(1.2, rel_136*100, srel_136*100)

print "\nrelative Energieaufloesung:"
print "\nEnergie    Si          CdTe"
print '59keV: %f        %f'%(rer_59_si, rer_59_cdte)
print '122keV: %f       %f'%(rer_122_si, rer_122_cdte)
print '136keV: %f       %f'%(rer_136_si, rer_136_cdte)

#now draw scaled pics
#scale it
scaled_cdte_am_x, scaled_cdte_co_x, scaled_si_am_x, scaled_si_co_x = [], [], [], []
for i in raw_cdte_am_x:
    scaled_cdte_am_x.append((i - cdte_b)/cdte_a)
for i in raw_cdte_co_x:
    scaled_cdte_co_x.append((i - cdte_b)/cdte_a)
for i in raw_si_am_x:
    scaled_si_am_x.append((i - si_b)/si_a)
for i in raw_si_co_x:
    scaled_si_co_x.append((i - si_b)/si_a)
count = len(scaled_cdte_am_x)
# Erzeuge Graphen
g = TGraph(count, array('d',scaled_cdte_am_x) ,array('d',raw_cdte_am_y))
g.SetTitle(';Energie [keV];Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(0, 100)
c = TCanvas('c_','')
c.SetGrid()
g.Draw('AP')
c.Update()


count = len(scaled_cdte_co_x)
# Erzeuge Graphen
g = TGraph(count, array('d',scaled_cdte_co_x) ,array('d',raw_cdte_co_y))
g.SetTitle(';Energie [keV];Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(0, 180)
c = TCanvas('c_','')
c.SetGrid()
g.Draw('AP')
c.Update()


count = len(scaled_si_am_x)
# Erzeuge Graphen
g = TGraph(count, array('d',scaled_si_am_x) ,array('d',raw_si_am_y))
g.SetTitle(';Energie [keV];Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(0, 100)
h = g.GetHistogram()
h.SetMinimum(0)
h.SetMaximum(20)
c = TCanvas('c_','')
c.SetGrid()
g.Draw('AP')
c.Update()


count = len(scaled_si_co_x)
# Erzeuge Graphen
g = TGraph(count, array('d',scaled_si_co_x) ,array('d',raw_si_co_y))
g.SetTitle(';Energie [keV];Counts')
g.GetHistogram().SetTitleOffset(1.3, 'Y')
g.SetMarkerStyle(3)
g.SetMarkerColor(2)
g.SetMarkerSize(1.0)
xa = g.GetXaxis()
xa.SetLimits(0, 180)
h = g.GetHistogram()
h.SetMinimum(0)
h.SetMaximum(300)
c = TCanvas('c_','')
c.SetGrid()
g.Draw('AP')
c.Update()

line = sys.stdin.readline()
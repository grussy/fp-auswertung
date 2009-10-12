#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
from array import array
from math import sqrt, log
from ROOT import gROOT, TCanvas, TGraphErrors, TF1, TLegend

gROOT.SetStyle("Plain")

# -------------------------------------------------------------------
# Lebensdauer des 3P1-Zustands
# -------------------------------------------------------------------

# Konstanten
hq  = 1.05457266e-34  # Planksches Wirkungsquantum
muB = 9.2740154e-24   # Bohrsches Magneton
gj  = 1.5             # Landscher Faktor

# Umrechnung der Temperatur [°C] in Druck [Torr]
def druck_falsch(T):
    if T >= -30 and T < 3.: A = 8.86; B = 0; C = -3440.
    elif T >= 3. and T <= 25: A = 10.6724; B = -0.847; C = -3342.26
    T += 273  # Temperatur von Celsius nach Kelvin
    return 10**A * 10**(C/T) * T**B

def druck(T):
    return 10**(8.86 - 3440/(T+273))

def schreibe_tabelle(name, mess, rchisq, w, sw, tau, stau):
    f = open(name+'.tex', 'w')
    f.write(r'''
\begin{tabular}{|c|c|c|c|c|c|}
\hline
Messung&$\chi^2/ndf$&$w\;/A$&$s_w\;/A$&$\tau\;/10^{-7}s$&$s_{\tau}\;/10^{-7}s$\\
\hline''')
    for i in range(len(mess)):
        f.write('%s&%f&%f&%f&%f&%f \\\\\n' % (
            mess[i], rchisq[i], w[i], sw[i], tau[i]*1e7, stau[i]*1e7))
    f.write(r'''\hline
\end{tabular}''')
    f.close()

def erzeuge_graphen(name, color=2, style=23):
    mess, rchisq, w, sw = [], [], [], []
    T, p, tau, stau = array('d'), array('d'), array('d'), array('d')
    for line in open(name, 'r'):
        tokens = line.split()
        Ti,wi,swi,rchisqi = map(float, tokens[1:])
        mess += [tokens[0]]; rchisq += [rchisqi]

        # berechne Lebensdauer aus Halbwertsbreite
        taui = hq / (gj * muB * 3.363e-4 * wi)
        staui = taui * swi/wi

        # berechne Druck aus Temperatur
        #pi = 10**(8.86-3440/(Ti+273))
	pi = druck_falsch(Ti)
        
        T.append(Ti)
        p.append(pi)
        tau.append(taui)
        stau.append(staui)
        w += [wi]; sw += [swi]
    
    # Fehler der Temperatureinzelmessung: 1°C
    #sT = array('d', [1.0/sqrt(2)]*len(T))
    sT = array('d', [5./9.]*len(T))

    # Fehler auf den Druck: C*log(10)*p*sT/T^2
    sp = array('d')
    for pi,Ti,sTi in zip(p,T,sT):
        spi = abs(-3440*log(10)*pi*sTi/(Ti+273)**2)
        sp.append(spi)

    # Schreibe Ergebnisse in Form einer TeX-Tabelle
    schreibe_tabelle(name, mess, rchisq, w, sw, tau, stau)

    # Graphen erstellen
    gT = TGraphErrors(len(T), T, tau, sT, stau)
    gT.SetTitle(';Temperatur T [#circC];Lebensdauer #tau [s]')
    gT.GetHistogram().SetTitleOffset(1.35, 'Y')
    gT.SetMarkerColor(color)
    gT.SetMarkerStyle(style)
    
    gp = TGraphErrors(len(p), p, tau, sp, stau)
    gp.SetTitle(';Druck p [Torr];Lebensdauer #tau [s]')
    gp.GetHistogram().SetTitleOffset(1.35, 'Y')
    gp.SetMaximum(0.14e-6)
    gp.SetMarkerColor(color)
    gp.SetMarkerStyle(style)

    return gT, gp

# Temperaturen und Halbwertsbreiten der 90° bzw. 0° Messreihe einlesen
gTa, gpa = erzeuge_graphen('fwhm90.dat')
gTb, gpb = erzeuge_graphen('fwhm0.dat', 4, 22)

# Linearer Fit der beiden Druck-Graphen
f = TF1('fa', '[0]*x + [1]')
f.SetParameter(0,1e-9); f.SetParameter(1,1e-7)

gpa.Fit(f, 'Q')
tau_a, stau_a = f.GetParameter(1), f.GetParError(1)
print '90°: tau = %g +- %g' % (tau_a, stau_a)

gpb.Fit(f, 'Q')
tau_b, stau_b = f.GetParameter(1), f.GetParError(1)
print '0°: tau = %g +- %g' % (tau_b, stau_b)

# Differenz der Ergebnisse berechnen
tau_diff = abs(tau_a - tau_b)
stau_diff = sqrt(stau_a**2 + stau_b**2)
print 'Differenz: %g +- %g' % (tau_diff, stau_diff)

# Graphen plotten
cT = TCanvas('cT', 'Lebensdauer des 3P1-Zustands, Temperatur')
cT.SetGrid()
gTa.Draw('AP')
gTb.Draw('P')
lp1 = TLegend(0.12, 0.88, 0.35, 0.80)
lp1.SetFillColor(0)
lp1.AddEntry(gpa, '90#circ Messreihe', 'p')
lp1.AddEntry(gpb, '0#circ Messreihe', 'p')
lp1.Draw()
cT.Update()

cp = TCanvas('cp', 'Lebensdauer des 3P1-Zustands, Druck')
cp.SetGrid()
gpa.Draw('AP')
gpb.Draw('P')
lp = TLegend(0.12, 0.88, 0.50, 0.70)
lp.SetFillColor(0)
lp.AddEntry(gpa, '90#circ Messreihe', 'p')
lp.AddEntry(gpa, '#tau = %.6g #pm %.6g' % (tau_a, stau_a), '')
lp.AddEntry(gpb, '0#circ Messreihe', 'p')
lp.AddEntry(gpb, '#tau = %.6g #pm %.6g' % (tau_b, stau_b), '')
lp.Draw()
cp.Update()
line = sys.stdin.readline()

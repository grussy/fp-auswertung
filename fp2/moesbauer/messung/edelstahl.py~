#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin, log, sqrt, exp
from konst import Q, c, hbar, E0, omega0
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors, TMath, TGaxis
from fit_tools import *
from scipy.special import jn

gROOT.SetStyle("Plain")

##########################################################################################
#                   Messung bei verschiedenen Geschwindigkeiten mit Edelstahlabsorber
# 
##########################################################################################

# Variablen, Datenfelder etc
messdaten = 'edelstahl_all.dat' #In dieser Datei befinden sich (bald) alle Messdaten / Unsortiert
untergrund = 50.38              #Untergrundrate für das Messfenster in cps
velo = []                       #Geschwindigkeiten des Schlittens
time = []                       #Dauer der Messung
counts = []                     #Gezählte Ereignisse
rates = []                      #Raten [counts/second]
srates = []                     #Fehler auf Raten
svelo = []                      #Fehler auf Geschwindigkeiten (bestimmt mit Maussensor)
stime = 0.1
scounts = 1
drawopts = 'APZ'

#Lade Daten:
print "Loading Data in %s ..."%(messdaten)
for line in open(messdaten):
    buffer = line.split()
    velo.append(float(buffer[0]))
    time.append(float(buffer[1]))
    counts.append(float(buffer[2]))
    rate = (float(buffer[2]) / (float(buffer[1]) / 1000)) - untergrund
    rates.append(rate)
    srates.append(rate*sqrt((stime/float(buffer[1]))**2+(sqrt(float(buffer[2]))/float(buffer[2]))**2))
length = len(velo)
svelo = [0.01]*length
assert length > 0
print "   found %i datapoints."%(length)

#print "Edelstahlabsorber, Messdaten: %s, Untergrund: %s cps" % (messdaten, untergrund)

#Plotte die Daten:
print "\nFitting and Drawing ..."
Fenster = TCanvas('cr', 'Edelstahlabsorber')
Fenster.SetGrid()
gr = TGraphErrors(length, array('d',velo), array('d', rates),array('d',svelo),array('d',srates))
gr.SetTitle('Edelstahlabsorber ( 1 Linie );Geschwindigkeit / mm/s; Zählrate 1/s')
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetHistogram().GetXaxis().SetLimits(-2.5, 2.5);
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')
frame = Fenster.GetFrame()
x1, x2, y2 = frame.GetX1(), frame.GetX2(), frame.GetY2()
E1 = (E0 / c * Q(-2.5,'mm/s')).inUnitsOf('eV').value
E2 = (E0 / c * Q(2.5,'mm/s')).inUnitsOf('eV').value
print E1
print E2
eax = TGaxis(x1, 0.5, x2, 0.5, E1, E2, 510, '')
eax.SetTitle('Energie [eV]')
eax.Draw()
eax.Paint()
Fenster.Update()
# Fuehre Lorentz-Fit durch:
fl = TF1('fl', '[0] + [1]*TMath::BreitWigner(x, [2], [3])')
fl.SetLineColor(3); fl.SetLineStyle(2); fl.SetLineWidth(2)
params = [
    (0, 'y_{0}',   270),
    (1, 'A',       -28),
    (2, '#mu',    0.2),
    (3, '#Gamma',  0.4) ]
for i, pn, pv in params:
    fl.SetParName(i, pn)
    fl.SetParameter(i, pv)
gr.Fit(fl, 'Q+')
#print_fit_result(fl)
lgl = create_fit_legend(
    fl, 'f(x)', 'Lorentz-Fit', lpos = (0.58, 0.41, 0.88, 0.64))
lgl.Draw()
print "   done with lorentz."
Fenster.Update()
# Fuehre Gauss-Fit durch:
fg = TF1('fg', '[0] + [1]*TMath::Gaus(x, [2], [3])')
fg.SetLineColor(4); fg.SetLineStyle(4); fg.SetLineWidth(2)
params = [
    (0, 'y_{0}',   267),
    (1, 'A',       -38),
    (2, '#mu',    0.2),
    (3, '#sigma',  0.2) ]
for i, pn, pv in params:
    fg.SetParName(i, pn)
    fg.SetParameter(i, pv)
gr.Fit(fg, 'Q+')
#print_fit_result(fg)
lgg = create_fit_legend(
    fg, 'f(x)', 'Gauss-Fit', lpos = (0.58, 0.16, 0.88, 0.38))
lgg.Draw()
print "   done with gauss."
Fenster.Update()
# Fuehre Voigt-Fit durch:
fv = TF1('fv', '[0] + [1]*TMath::Voigt(x-[2], [3], [4])')
fv.SetLineColor(1); fv.SetLineStyle(1); fv.SetLineWidth(2)
fv.SetNpx(1000)
params = [
    (0, 'y_{0}',   269), # 135
    (1, 'A',       -25),
    (2, '#mu',    0.22),
    (3, '#sigma',  0.13),
    (4, '#Gamma',  0.2) ]
for i, pn, pv in params:
    fv.SetParName(i, pn)
    fv.SetParameter(i, pv)
gr.Fit(fv, 'Q+')
#print_fit_result(fv)
lgv = create_fit_legend(
    fv, 'f(x)', 'Faltung von Lorentz und Gauss',
    lpos = (0.13, 0.16, 0.43, 0.38))
lgv.Draw()
print "   done with voigt."
Fenster.Update()
print "   all done."



# Berechen gesuchte Werte -------------------------------------------------
print "\nLorentzFit"
# Lorentz, Fitparameter Gamma
mu, smu = fl.GetParameter(3), fl.GetParError(3)
Gmess, sGmess = Q(mu, 'mm/s'), Q(smu, 'mm/s')
W, sW = 4.15, 0.1
print 'Gemessene Linienbreite: (%g +- %g) mm/s  (%.2f%%)' % (
    Gmess.value, sGmess.value, abs(sGmess.value/Gmess.value)*100)
Gmess = (E0 * Gmess/ c).inUnitsOf('eV')
sGmess =  (E0 * sGmess / c).inUnitsOf('eV')
print 'Gemessene Linienbreite: (%g +- %g) eV  (%.2f%%)' % (
    Gmess.value, sGmess.value, abs(sGmess.value/Gmess.value)*100)
Gmess = (E0 *  Q(mu/W, 'mm/s')/ c).inUnitsOf('eV')
sGmess = Gmess * sqrt((sW/W)**2+(smu/mu)**2)
print 'natürl Linienbreite: (%g +- %g) eV  (%.2f%%)' % (
    Gmess.value, sGmess.value, abs(sGmess/Gmess)*100)
tau = (hbar/Gmess).inUnitsOf('ns')
stau = tau*(sGmess/Gmess)
print 'Mittlere Lebensdauer: (%g +- %g) ns (%.2f%%)' % (
    tau.value, stau.value, abs(stau/tau)*100)

print "\nVoigtFit"
w, sw = Q(fv.GetParameter(4), 'mm/s'), Q(fv.GetParError(4), 'mm/s')     # Halbwertsbreite [mm/s]
mu, smu = Q(fv.GetParameter(2), 'mm/s'), Q(fv.GetParError(2), 'mm/s') # Isomerieverschiebung [mm/s]
# Isomerieverschiebung [eV]
Eiso = (E0 * mu / c).inUnitsOf('eV')
sEiso = (E0 * smu / c).inUnitsOf('eV')
print 'Isomerieverschiebung: (%g +- %g) eV  (%.2f%%)' % (
    Eiso.value, sEiso.value, abs(sEiso/Eiso)*100)
# Gemessene Linienbreite [eV]
Gmess = (E0 * w / c).inUnitsOf('eV')
sGmess = (E0 * sw / c).inUnitsOf('eV')
print 'Gemessene Linienbreite: (%g +- %g) eV  (%.2f%%)' % (
    Gmess.value, sGmess.value, abs(sGmess/Gmess)*100)
# Angegebene Werte
n = 0.7*Q('8.4e22 cm**(-3)')     # Anzahl der Eisenatome pro cm^3
beta = 0.022                     # Anteil von Fe-57
alpha, salpha = 8.9, 0.7         # Konversionskoeffizient alpha
fa = 0.8                         # Debye-Waller Faktor des Absorbers
da = Q('25 mum').inUnitsOf('m')  # Dicke des Absorbers [m]

# Wirkungsquerschnitt [m^2]
sigma0 = (2*pi * (c/omega0)**2 * 1./(1.+alpha) * 4./2.).inUnitsOf('m**2')
ssigma0 = sigma0 * salpha/(1.+alpha)

# Effektive Absorberdicke
da_eff = beta * fa * da * n * sigma0
sda_eff = da_eff * ssigma0/sigma0
print 'Effektive Absorberdicke: %g +- %g (%.2f%%)' % (
    da_eff, sda_eff, sda_eff/da_eff*100)
#Debye-Waller-Faktor der Quelle
Zmin ,sZmin = 228.5, 0.2
Zmax, sZmax = 270, 0.2
f_Q = ((Zmax-Zmin)/Zmax)*(1-exp(-da_eff/2)* jn(0,1j*(da_eff/2)) )**(-1)
sf_Q = f_Q*(sda_eff/da_eff)
print 'Debye-Waller-Faktor der Quelle: %g +- %g (%.2f%%)' % (
    f_Q, sf_Q, sf_Q/f_Q*100)
# Natuerliche Linienbreite [eV] (duenne Absorber / Voigt-Fit)
G = Gmess / 2
sG = sGmess / 2
print 'Natuerliche Linienbreite: (%g +- %g) eV  (%.2f%%)' % (
    G.value, sG.value, abs(sG/G)*100)
# Mittlere Lebensdauer [ns]
tau = (hbar/G).inUnitsOf('ns')
stau = tau * sG/G
print 'Mittlere Lebensdauer: (%g +- %g) ns (%.2f%%)' % (
    tau.value, stau.value, abs(stau/tau)*100)
# maximaler Wirkungsquerschnitt
sig = sigma0.inUnitsOf('m*m').value
ssig = ssigma0.inUnitsOf('m*m').value
print 'Wirkungsquerschnitt: (%g +- %g) m^2 (%.2f%%)' % (
    sig, ssig, ssig/sig*100)






print "\nDone. Press Enter to continue ..."
raw_input();

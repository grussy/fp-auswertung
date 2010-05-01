#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin, log
from konst import Q, c, hbar, E0, omega0
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors, TMath, TGaxis
from fit_tools import *

gROOT.SetStyle("Plain")

##########################################################################################
#                   Messung bei verschiedenen Geschwindigkeiten mit Edelstahlabsorber
# 
##########################################################################################

# Variablen, Datenfelder etc
messdaten = 'edelstahl_all.dat' #In dieser Datei befinden sich (bald) alle Messdaten / Unsortiert
untergrund = 50.38              #Untergrundrate f�r das Messfenster in cps
velo = []                       #Geschwindigkeiten des Schlittens
time = []                       #Dauer der Messung
counts = []                     #Gez�hlte Ereignisse
rates = []                      #Raten [counts/second]
srates = []                     #Fehler auf Raten
svelo = []                      #Fehler auf Geschwindigkeiten (bestimmt mit Maussensor)

#Lade Daten:
print "Loading Data in %s ..."%(messdaten)
for line in open(messdaten):
    buffer = line.split()
    velo.append(float(buffer[0]))
    time.append(float(buffer[1]))
    counts.append(float(buffer[2]))
    rates.append((float(buffer[2]) / (float(buffer[1]) / 1000)) - untergrund)
length = len(velo)
assert length > 0
print "   found %i datapoints."%(length)

#print "Edelstahlabsorber, Messdaten: %s, Untergrund: %s cps" % (messdaten, untergrund)

#Plotte die Daten:
print "\nFitting and Drawing ..."
Fenster = TCanvas('cr', 'Edelstahlabsorber')
Fenster.SetGrid()
gr = TGraph(length, array('d',velo), array('d', rates))
gr.SetTitle('Edelstahlabsorber ( 1 Linie );Geschwindigkeit / mm/s; Z�hlrate 1/s')
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')

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

# Fuehre Voigt-Fit durch:
fv = TF1('fv', '[0] + [1]*TMath::Voigt(x-[2], [3], [4])')
fv.SetLineColor(1); fv.SetLineStyle(1); fv.SetLineWidth(2)
fv.SetNpx(1000)
params = [
    (0, 'y_{0}',   269), # 135
    (1, 'A',       -25),
    (2, '#mu',    0.22),
    (3, '#sigma',  0.13),
    (4, '#Gamma',  0.26) ]
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

def fwhm(f, xl=-30.0, xr=30.0):
    '''
    Berechnet volle Breite des halben Maximums.
    Dabei wird die Funktion f im Bereich xl <= x <=xr untersucht.
    '''
    ymax, xmin = f.GetParameter(0), f.GetParameter(2)
    yh = (ymax + f.Eval(xmin))/2.0
    return f.GetX(yh, xmin, xr) - f.GetX(yh, xl, xmin)


# Voigt, FWHM
## mu, smu = fv.GetParameter(2), fv.GetParError(2)
## w, sw = fwhm(fv), abs(fwhm(fg)-fwhm(fl))/2

# Voigt, Fitparameter Gamma
mu, smu = fv.GetParameter(2), fv.GetParError(2)
w, sw = fv.GetParameter(4), fv.GetParError(4)

# Lorentz, Fitparameter Gamma
## mu, smu = fl.GetParameter(2), fl.GetParError(2)
## w, sw = fl.GetParameter(3), fl.GetParError(3)

w, sw = Q(w, 'mm/s'), Q(sw, 'mm/s')     # Halbwertsbreite [mm/s]
mu, smu = Q(mu, 'mm/s'), Q(smu, 'mm/s') # Isomerieverschiebung [mm/s]


# Isomerieverschiebung [eV]
Eiso = (E0 * mu / c).inUnitsOf('eV')
sEiso = (E0 * smu / c).inUnitsOf('eV')

# Gemessene Linienbreite [eV]
Gmess = (E0 * w / c).inUnitsOf('eV')
sGmess = (E0 * sw / c).inUnitsOf('eV')

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

# Natuerliche Linienbreite [keV] (lineare Naeherung)
## G = Gmess / (2. + 0.27 * da_eff)
## sG = G/Gmess * (
## sGmess**2 + (0.27 * beta * fa * da * n * ssigma0 * G)**2)**(0.5)

# Natuerliche Linienbreite [keV] (polynomielle Naeherung nach Heberle)
## t, st = da_eff, sda_eff
## a1, a2, a3, a4 = 0.1288, 4.733e-3, -9.21e-4, 3.63e-5
## G = 0.5*Gmess / (1. + a1*t + a2*t**2 + a3*t**3 + a4*t**4)
## sG = G * ( (sGmess/Gmess)**2 +
##            ( st * (a1 + 2*a2*t + 3*a3*t**2 + 4*a4*t**3)/
##              (1. + a1*t + a2*t**2 + a3*t**3 + a4*t**4) )**2
##          )**0.5

# Natuerliche Linienbreite [eV] (Relative Verbreiterung W abgelesen)
## W, sW = 3.63, 0.09
## G = Gmess / W
## sG = G * ( (sGmess/Gmess)**2 + (sW/W)**2 )**0.5

# Natuerliche Linienbreite [eV] (duenne Absorber / Voigt-Fit)
G = Gmess / 2
sG = sGmess / 2

# Mittlere Lebensdauer [ns]
tau = (hbar/G).inUnitsOf('ns')
stau = tau * sG/G

# Halbwertszeit [ns]
t12 = tau * log(2)
st12 = stau * log(2)

print '\nIsomerieverschiebung: (%g +- %g) eV  (%.2f%%)' % (
    Eiso.value, sEiso.value, abs(sEiso/Eiso)*100)
print 'Effektive Absorberdicke: %g +- %g (%.2f%%)' % (
    da_eff, sda_eff, sda_eff/da_eff*100)
print 'Gemessene Linienbreite: (%g +- %g) eV  (%.2f%%)' % (
    Gmess.value, sGmess.value, abs(sGmess/Gmess)*100)
print 'Natuerliche Linienbreite: (%g +- %g) eV  (%.2f%%)' % (
    G.value, sG.value, abs(sG/G)*100)
print 'Mittlere Lebensdauer: (%g +- %g) ns (%.2f%%)' % (
    tau.value, stau.value, abs(stau/tau)*100)
print 'Halbwertszeit: (%g +- %g) ns (%.2f%%)' % (
    t12.value, st12.value, abs(st12/t12)*100)


print "\nDone. Press Enter to continue ..."
raw_input();
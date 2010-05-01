#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#from konst import phi0, omega, somega
from math import pi, cos, sin, sqrt
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
from Scientific.Physics.PhysicalQuantities import PhysicalQuantity as Q
from fit_tools import *
gROOT.SetStyle("Plain")
##########################################################################################
#                   Messung bei verschiedenen Geschwindigkeiten mit Eisenabsorber
# 
##########################################################################################

# Variablen, Datenfelder etc
messdaten = 'eisen_all.dat'     #In dieser Datei befinden sich (bald) alle Messdaten / Unsortiert
untergrund = 50.38              #Untergrundrate f�r das Messfenster in cps
velo = []                       #Geschwindigkeiten des Schlittens
time = []                       #Dauer der Messung
counts = []                     #Gez�hlte Ereignisse
rates = []                      #Raten [counts/second]
srates = []                     #Fehler auf Raten
svelo = []                      #Fehler auf Geschwindigkeiten (bestimmt mit Maussensor)
stime = 2
scounts = 1

#Physikalische konstanten
# Lichtgeschwindigkeit [m/s]
c = Q('1c').inUnitsOf('m/s')
# Wirkungsquantum
hbar = Q('1hbar').inUnitsOf('J*s')
# Energie des Gamma-Uebergangs [keV] (Quelle: www.nndc.bnl.gov)
E0 = Q('14.4128 keV')
# Kreisfrequenz des Gamma-Quants [1/s]
omega0 = (E0/hbar).inUnitsOf('1/s')
# Kernmagneton [MeV/T]
muN = Q('3.15245166e-14 MeV/T')
#Fitparameter
params = [
    (0, 'y_{0}',   265.61),
    (1, 'A1',       -13),
    (2, '#w1',    0.6),
    (3, '#wc1',  -5),
    
    (4, 'A2',       -6),
    (5, '#w2',    0.4),
    (6, '#wc2',  -3), 

    (7, 'A3',       -4.5),
    (8, '#w3',    0.2),
    (9, '#wc3',  -0.7), 

    (10, 'A4',       -4),
    (11, '#w4',    0.25),
    (12, '#wc4',  0.9), 

    (13, 'A5',       -8),
    (14, '#w5',    0.3),
    (15, '#wc5',  3), 

    (16, 'A6',       -16),
    (17, '#w6',    0.9),
    (18, '#wc6',  5)]
#Sortiert die Peaks, die indizes sind die der Parameter der peaks s.o.
sort = [12, 9, 15, 6, 18, 3]

# Hilfsfunktionen
def gew_mittel(xsx):
    '''gew_mittel(list(float,float)) -> (float, float)
    xsx  : Liste aus Tupeln der Messwerte mit jeweiligen Fehlern
    ->   Tupel (gx, sgx) aus gewichtetem Mittel und dessen Fehler'''
    suma = 0. * xsx[0][0] / xsx[0][1]**2
    sumb = 0. * 1. / xsx[0][1]**2
    for xi,sxi in xsx:
        suma += xi / sxi**2
        sumb += 1. / sxi**2
    return (suma/sumb, sumb**(-0.5))
def arith_mittel(x):
    '''arith_mittel(list(float)) -> float
    x  : Liste aus Messwerte
    ->   arithmetisches Mittel der Messwerte'''
    sumx = 0. * x[0]
    for xi in x:
        sumx += xi
    return sumx / len(x)

# START DES SCRIPTS
##########################################################################################

print "Loading ..."
for line in open(messdaten):
    if (not line.strip()) or (line.strip()[0] == '#'): continue
    buffer = line.split();
    velo.append(float(buffer[0]))
    time.append(float(buffer[1]))
    counts.append(float(buffer[2]))
    rate = (float(buffer[2]) / (float(buffer[1]) / 1000)) - untergrund
    rates.append(rate)
    srates.append(rate*sqrt((stime/float(buffer[1]))**2+(sqrt(float(buffer[2]))/float(buffer[2]))**2))
length = len(velo)
svelo = [0.01]*length
print " found %i datapoints"%(length)

#Plotte die Daten:
drawopts = 'APZ'
print "\nFitting and Drawing ..."
Fenster = TCanvas('cr', 'Eisenabsorber')
Fenster.SetGrid()
gr = TGraphErrors(length, array('d',velo), array('d', rates), array('d',svelo), array('d', srates))
gr.SetTitle(';Geschwindigkeit / mm/s; Z�hlrate 1/s')
gr.GetHistogram().GetXaxis().SetLimits(-10.0, 10.0);
gr.GetHistogram().SetTitleOffset(1.3, 'Y')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw(drawopts)


# 6-Fach Loretzfit -----------------------------------------------------------

#erzeuge Fitfunktion
lorentz = '[0]'  #Offset
for i in range(1,7):
    j = 3*i
    lorentz += '+ 2*[%i]/pi * [%i]/(4*(x-[%i])^2 + [%i]^2)' % (j-2,j-1,j,j-1)

f = TF1('f', lorentz)

for i, pn, pv in params:
    f.SetParName(i, pn)
    f.SetParameter(i, pv)

gr.Fit(f, 'Q+',drawopts)
lg = TLegend(0.7, 0.8, 1, 1)
lg.SetFillColor(0)
lg.SetHeader('')
lg.AddEntry(f, '6-facher Lorentzfit', 'l')
for peak in sorted(sort):
    i = 0
    for t in sort:
        i += 1
        if (t == peak):
            break        
    lg.AddEntry(f, 'Peak %i = %.4g #pm %.4g' % ( i,
        f.GetParameter(peak), f.GetParError(peak)), '')
ndf = f.GetNDF()
if ndf > 0:
    chisq = f.GetChisquare()
    lg.AddEntry(f, '#chi^{2}/ndf = %.2f/%d = %.2f' % (
        chisq, ndf, chisq/ndf), '')
lg.Draw(drawopts)
Fenster.Update()
print " done."

# Calculations and Results:
print "\nCalculating Results ..."
# Absorptionsminima [mm/s]
v = [Q(n, 'mm/s') for n in map(f.GetParameter , sort)]
sv = [Q(n, 'mm/s') for n in map(f.GetParError , sort)]

# Absorptionsminima [eV]
E = [(E0 * vi / c).inUnitsOf('eV') for vi in v]
sE = [(E0 * svi / c).inUnitsOf('eV') for svi in sv]

print '\n Absorptionsminima:'
for i in range(len(v)):
    print '\t%d: (%.4g +- %.4g)mm/s\t(%.4g +- %.4g)eV\t(%.2f%%)' % (
        (i+1),
        v[i].value, sv[i].value,
        E[i].value, sE[i].value,
        abs(sv[i].value/v[i].value*100))
    

# Isomerieverschiebung [mm/s]
viso = [(v[2*i] + v[2*i+1])/2 for i in range(len(v)/2)]
sviso = [0.5*(sv[2*i]**2 + sv[2*i+1]**2)**(0.5) for i in range(len(v)/2)]
mviso, msviso = gew_mittel(zip(viso, sviso))

# Isomerieverschiebung [eV]
Eiso = [(E0 * vi / c).inUnitsOf('eV') for vi in viso]
sEiso = [(E0 * svi / c).inUnitsOf('eV') for svi in sviso]
mEiso, msEiso = gew_mittel(zip(Eiso, sEiso))

print '\n Isomerieverschiebung:'
for i in range(len(viso)):
    print '\t%d: (%.4g +- %.4g)mm/s\t(%.4g +- %.4g)eV\t(%.2f%%)' % (
        (i+1),
        viso[i].value, sviso[i].value,
        Eiso[i].value, sEiso[i].value,
        abs(sviso[i].value / viso[i].value * 100))

print ' gewichtetes Mittel:'
print '\t   (%.4g +- %.4g)mm/s\t(%.4g +- %.4g)eV\t(%.2f%%)' % (
        mviso.value, msviso.value,
        mEiso.value, msEiso.value,
        abs(msviso / mviso * 100))


# Kernmagnetisches Moment des Grundzustands von Fe-57 (Quelle: nndc)
mug = 0.09044 * muN
smug = 0.00007 * muN

# Kernmagnetisches Moment des 14keV-Zustands von Fe-57 (Quelle: nndc)
mua = -0.1549 * muN
smua = 0.0002 * muN

# Differenzen zwischen den jeweiligen Peaks [mm/s]
dv = [v[2*i]-v[2*i+1] for i in range(len(v)/2)]
sdv = [(sv[2*i]**2 + sv[2*i+1]**2)**(0.5) for i in range(len(sv)/2)]

# Kernmagnetisches Moment des 14.4keV Zustands [MeV/T]
mua_12 = 3*mug*(dv[0]-dv[1])/(dv[0]+dv[1])
a, b = dv[0]-dv[1], dv[0]+dv[1]
smua_12 = abs(mua_12) * ( (smug/mug)**2 + (1/a-1/b)**2 * sdv[0]**2
                          + (1/a+1/b)**2 * sdv[1]**2 )**(0.5)

mua_23 = mug*(dv[1]-dv[2])/(dv[1]-dv[2]/3)
a, b = dv[1]-dv[2], 3*dv[1]-dv[2]
smua_23 = abs(mua_23) * ( (smug/mug)**2 + (1/a-3/b)**2 * sdv[1]**2
                          + (1/a-1/b)**2 * sdv[2]**2 )**(0.5)

mua_31 = mug*(dv[0]-dv[2])/(dv[0]+dv[2]/3)
a, b = -dv[2]+dv[0], dv[2]+dv[0]
smua_31 = abs(mua_31) * ( (smug/mug)**2 + (1/a+1/b)**2 * sdv[2]**2
                          + (1/a-3/b)**2 * sv[0]**2 )**(0.5)

print '\n Kernmagnetisches Moment:'
print '\tmua_12: (%.4g +- %.4g)muN\t(%.2f%%)' % (
    mua_12/muN, smua_12/muN, abs(smua_12/mua_12*100))
print '\tmua_23: (%.4g +- %.4g)muN\t\t(%.2f%%)' % (
    mua_23/muN, smua_23/muN, abs(smua_23/mua_23*100))
print '\tmua_31: (%.4g +- %.4g)muN\t(%.2f%%)' % (
    mua_31/muN, smua_31/muN, abs(smua_31/mua_31*100))



# Magnetfeld am Kernort [T]
B1 = (dv[0]*E0 / (2*c*(mua/3 + mug))).inUnitsOf('T')
sB1 = B1 * ((sdv[0]/dv[0])**2
            + (smua/(mua+3*mug))**2 + (smug/(mua/3+mug))**2)**0.5

B2 = (dv[1]*E0 / (2*c*(-mua/3 + mug))).inUnitsOf('T')
sB2 = B2 * ((sdv[1]/dv[1])**2
            + (smua/(-mua+3*mug))**2 + (smug/(-mua/3+mug))**2)**0.5

B3 = (dv[2]*E0 / (2*c*(-mua + mug))).inUnitsOf('T')
sB3 = B3 * ((sdv[2]/dv[2])**2
            + (smua/(-mua+mug))**2 + (smug/(-mua+mug))**2)**0.5

B, sB = gew_mittel([(B1,sB1), (B2,sB2), (B3,sB3)])

print '\n Magnetfeld am Kernort:'
print '\tB1: (%.4g +- %.4g)T\t(%.2f%%)' % (
    B1.value, sB1.value, sB1/B1*100)
print '\tB2: (%.4g +- %.4g)T\t(%.2f%%)' % (
    B2.value, sB2.value, sB2/B2*100)
print '\tB3: (%.4g +- %.4g)T\t(%.2f%%)' % (
    B3.value, sB3.value, sB3/B3*100)
print ' gewichtetes Mittel:'
print '\t    (%.4g +- %.4g)T\t\t(%.2f%%)' % (
    B.value, sB.value, sB/B*100)
print "\nScript Done. Press Enter to finish ..."
raw_input();
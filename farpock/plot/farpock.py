#!/usr/bin/python


import sys
from array import array
from math import sqrt, log
from ROOT import gROOT, TCanvas, TGraphErrors, TF1, TLegend

gROOT.SetStyle("Plain")

#Pockelszelle Saegezahn
print "-----------------Pockelszelle Saegezahn--------------------"

#Spannungseichung

UssMit = 0.162
UssOhne = 17.6

Uumrechnung = UssOhne / UssMit

print "Umrechnungsfaktor fuer Spannungsteiler: %.2f" % Uumrechnung

#Saegezahn

Ulambdahalbe = [2.32, 2.28, 2.24, 2.28, 2.33]
sUlambdahalbe = 0.08
U = []
sU = sUlambdahalbe * Uumrechnung

print "Messdaten"
for i in Ulambdahalbe:
	print " %.2f +- %.2f" % (i, sUlambdahalbe) 
	U += [i * Uumrechnung]


print "Spannung an der Pockelzelle (Umgerechnet)"
for i in U:
	print " %.2f +- %.2f" % (i, sU)

#Mittelwert
print "Mittelwert"
Umittel = sum(U) / len(U)
sUmittel = sU / sqrt(len(U))
print "%.2f +- %.2f" % (Umittel, sUmittel)


#Pockelszelle Sinus
print "-----------------------Pockelszelle Sinus-------------------------"

#lese Messdaten
Ulam2 = []

for line in open("data/sinus.dat", 'r'):
        tokens = line.split()
        nummer, Uimax, Uimin  = map(float, tokens)
        Ulam2 += [Uimax - Uimin]
	print "Umax = %.2f , Umin = %.2f , Umax - Umin = %.2f" % ( Uimax, Uimin, Uimax - Uimin )

#Mittelwert
print "Mittelwert"
Umittel2 = - sum(Ulam2) / len(Ulam2)
sUmittel2 = 1.2
print "%.2f +- %.2f" % (Umittel2, sUmittel2)

#gewichtetes Mittel aus Beiden Messreihen
print "-------------------Gewichtetes Mittel aus Beiden Messreihen----------------------"
gMittel = sum([Umittel2/sUmittel2, Umittel/sUmittel]) / sum([ 1/sUmittel2, 1/sUmittel])
sgMittel = 1 / sum([ 1/sUmittel2, 1/sUmittel])
print "Ulambdahalbe = %.2f +- %.2f" % (gMittel, sgMittel)

#Berechnung des elektrooptischen Koeffizienten
n1 = 1.522
n3 = 1.477
d = 2.4e-3
l = 20e-3
laserlambda = 632.8e-9

r41 = laserlambda * d / 4 / l / gMittel * 0.5 * sqrt((1/(n1**2) + 1/(n3**2))**3)
sr41 = r41 * sgMittel / gMittel

print "r41 = %.3e +- %.3e" % ( r41, sr41 )

#Faradayeffekt
print "-------------------Faradayeffekt----------------------"
#lese Messdaten
I, Phi = [], []
sI = [0.05]

for line in open("data/faraday.dat", 'r'):
        tokens = line.split()
        Ii, sIi, Phi1, Phi2, Phi3, Phi4, sPhi = map(float, tokens)
	if Phi1 > 20. :
		Phi1 -= 180.
	if Phi2 > 20. :
		Phi2 -= 180.
	if Phi3 > 20. :
		Phi3 -= 180.
	if Phi4 > 20. :
		Phi4 -= 180.
	Phimittel = sum([Phi1, Phi2, Phi3, Phi4]) / 4
        I += [Ii]
	Phi += [Phimittel]
	print "I = %.2f -- -- Phimittel = %.2f" % ( Ii, Phimittel )

#plotte Daten
count = len(I)
sI = [0.05]*count
sPhi = [0.05/sqrt(4)]*count
cr = TCanvas('cr', 'Faradayeffekt')
cr.SetGrid()
gr = TGraphErrors(count, array('d',I), array('d', Phi),
                  array('d',sI), array('d',sPhi))
gr.SetTitle(';Spulenstrom I [A]; Winkel Phi [Grad]')
gr.GetYaxis().CenterTitle()
gr.SetMarkerColor(2)
gr.SetMarkerStyle(3)
gr.Draw('AP')

# Linearer Fit
fr = TF1('fr', '[0]*x + [1]')
gr.Fit(fr, 'Q')
ar, sar = fr.GetParameter(0), fr.GetParError(0)
br, sbr = fr.GetParameter(1), fr.GetParError(1)
chisqr = fr.GetChisquare()

lr = TLegend(0.55, 0.54, 0.88, 0.84)
lr.SetFillColor(0)
lr.AddEntry(gr, 'Messdaten', 'p')
lr.AddEntry(fr, 'Linearer Fit: Phi = ax + b', 'l')
lr.AddEntry(fr, 'a = %.2f #pm %.2f' % (ar,sar), '')
lr.AddEntry(fr, 'b = %.2g #pm %.2g' % (br,sbr), '')
lr.AddEntry(fr, '#chi^{2} = %.4g' % fr.GetChisquare(), '')
lr.Draw()
cr.Update()

print "Fitparameter Phi = ax + b"
print 'a: %.5e +- %.5e,' % (ar,sar),
print 'b: %.5g +- %.5g' % (br,sbr)
print "Chisquare: %.2f" % chisqr

#Berechnung der Verdetkonstanten
V = ar * (1./2556)
print "Verdetkonstante V = %.2e" % V

#Umrechnung
print "Nach Umrechnung:"
uV = V * 60. / 1.2564
print "Verdetkonstante V = %.2e" %uV










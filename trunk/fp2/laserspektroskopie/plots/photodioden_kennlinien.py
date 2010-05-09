#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from konst import phi0, omega, somega
from math import pi, cos, sin
from array import array
import sys; sys.path.append('/usr/lib/root/')
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors

gROOT.SetStyle("Plain")

Diode1_laserstrom = []
Diode1_U_50R = []
Diode1_U_1K = []
Diode1_U_10K = []

for line in open('../daten/PD1_kennlinie.dat','r'):
    if not line.strip() or line.strip()[0] == '#': continue
    splitted = line.split()
    Diode1_laserstrom.append(float(splitted[0]))
    Diode1_U_50R.append(float(splitted[1]))
    Diode1_U_1K.append(float(splitted[2]))
    Diode1_U_10K.append(float(splitted[3]))
    
    
#TODO: Errors Y from Oszilloskope File anf�gen

graphD1_50R = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_50R), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_50R)))
    
graphD1_1K = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_1K), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_1K)))
            
graphD1_10K = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_10K), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_10K)))


canvasD1 = TCanvas('Diode 1', 'Photo1')
canvasD1.SetGrid()
graphD1_10K.SetTitle('Photodiode 1;Laserstrom [mA]; Photodiodenspannung [mV]')
graphD1_10K.Draw('A*')
graphD1_10K.SetMarkerColor(2)
graphD1_10K.SetMarkerStyle(3)
graphD1_1K.Draw('*')
graphD1_1K.SetMarkerColor(3)
graphD1_1K.SetMarkerStyle(3)
graphD1_50R.Draw('*')
graphD1_50R.SetMarkerColor(4)
graphD1_50R.SetMarkerStyle(3)
lg1 = TLegend(0.7, 0.8, 1, 1)
lg1.SetFillColor(0)
lg1.SetHeader('Wiederstaende')
lg1.AddEntry(graphD1_10K, '10 kOhm', 'p')
lg1.AddEntry(graphD1_1K, '1 kOhm', 'p')
lg1.AddEntry(graphD1_50R, '50 Ohm', 'p')
lg1.Draw()
canvasD1.Update()

# 2te Photodiode: ----------------------------------------------------------------
Diode2_laserstrom = []
Diode2_U_50R = []
Diode2_U_1K = []
Diode2_U_10K = []

for line in open('../daten/PD2_kennlinie.dat','r'):
    if not line.strip() or line.strip()[0] == '#': continue
    splitted = line.split()
    Diode2_laserstrom.append(float(splitted[0]))
    Diode2_U_50R.append(float(splitted[1]))
    Diode2_U_1K.append(float(splitted[2]))
    Diode2_U_10K.append(float(splitted[3]))


#TODO: Errors Y from Oszilloskope File anf�gen
graphD2_50R = TGraphErrors(len(Diode2_laserstrom), array('d',Diode2_laserstrom) ,array('d',Diode2_U_50R), 
            array('d',[1]*len(Diode2_laserstrom)), array('d',[2]*len(Diode2_U_50R)))
    
graphD2_1K = TGraphErrors(len(Diode2_laserstrom), array('d',Diode2_laserstrom) ,array('d',Diode2_U_1K), 
            array('d',[1]*len(Diode2_laserstrom)), array('d',[2]*len(Diode2_U_1K)))
            
graphD2_10K = TGraphErrors(len(Diode2_laserstrom), array('d',Diode2_laserstrom) ,array('d',Diode2_U_10K), 
            array('d',[1]*len(Diode2_laserstrom)), array('d',[2]*len(Diode2_U_10K)))


canvasD2= TCanvas('Diode 2', 'Photo2')
canvasD2.SetGrid()
graphD2_10K.SetTitle('Photodiode 2;Laserstrom [mA]; Photodiodenspannung [mV]')
graphD2_10K.Draw('A*')
graphD2_10K.SetMarkerColor(2)
graphD2_10K.SetMarkerStyle(3)
graphD2_1K.Draw('*')
graphD2_1K.SetMarkerColor(3)
graphD2_1K.SetMarkerStyle(3)
graphD2_50R.Draw('*')
graphD2_50R.SetMarkerColor(4)
graphD2_50R.SetMarkerStyle(3)
lg2 = TLegend(0.7, 0.8, 1, 1)
lg2.SetFillColor(0)
lg2.SetHeader('Wiederstaende')
lg2.AddEntry(graphD2_10K, '10 kOhm', 'p')
lg2.AddEntry(graphD2_1K, '1 kOhm', 'p')
lg2.AddEntry(graphD2_50R, '50 Ohm', 'p')
lg2.Draw()


canvasD2.Update()

print "\nDone. Press Enter to continue ..."
raw_input();
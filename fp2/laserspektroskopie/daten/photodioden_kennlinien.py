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

for line in open('PD1_kennlinie.dat','r'):
    if not line.strip() or line.strip()[0] == '#': continue
    splitted = line.split()
    Diode1_laserstrom.append(float(splitted[0]))
    Diode1_U_50R.append(float(splitted[1]))
    Diode1_U_1K.append(float(splitted[2]))
    Diode1_U_10K.append(float(splitted[3]))
    
    
#TODO: Errors Y from Oszilloskope File anfügen

graphD1_50R = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_50R), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_50R)))
    
graphD1_1K = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_1K), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_1K)))
            
graphD1_10K = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_10K), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_10K)))


canvasD1 = TCanvas('Diode 1', 'Photo1')
canvasD1.SetGrid()
graphD1_10K.Draw('AC*')
graphD1_1K.Draw('C*')
graphD1_50R.Draw('C*')

canvasD1.Update()

# 2te Photodiode: ----------------------------------------------------------------
Diode2_laserstrom = []
Diode2_U_50R = []
Diode2_U_1K = []
Diode2_U_10K = []

for line in open('PD2_kennlinie.dat','r'):
    if not line.strip() or line.strip()[0] == '#': continue
    splitted = line.split()
    Diode2_laserstrom.append(float(splitted[0]))
    Diode2_U_50R.append(float(splitted[1]))
    Diode2_U_1K.append(float(splitted[2]))
    Diode2_U_10K.append(float(splitted[3]))


#TODO: Errors Y from Oszilloskope File anfügen
graphD2_50R = TGraphErrors(len(Diode2_laserstrom), array('d',Diode2_laserstrom) ,array('d',Diode2_U_50R), 
            array('d',[1]*len(Diode2_laserstrom)), array('d',[2]*len(Diode2_U_50R)))
    
graphD2_1K = TGraphErrors(len(Diode2_laserstrom), array('d',Diode2_laserstrom) ,array('d',Diode2_U_1K), 
            array('d',[1]*len(Diode2_laserstrom)), array('d',[2]*len(Diode2_U_1K)))
            
graphD2_10K = TGraphErrors(len(Diode2_laserstrom), array('d',Diode2_laserstrom) ,array('d',Diode2_U_10K), 
            array('d',[1]*len(Diode2_laserstrom)), array('d',[2]*len(Diode2_U_10K)))


canvasD2= TCanvas('Diode 2', 'Photo2')
canvasD2.SetGrid()
graphD2_10K.Draw('AC*')
graphD2_1K.Draw('C*')
graphD2_50R.Draw('C*')

canvasD2.Update()

print "\nDone. Press Enter to continue ..."
raw_input();
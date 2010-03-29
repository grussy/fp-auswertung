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
    Diode1_laserstrom.append(splitted[0])
    Diode1_U_50R.append(splitted[1])
    Diode1_U_1K.append(splitted[2])
    Diode1_U_10K.append(splitted[3])

graphD1_50R = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_50R), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_50R)))
    
graphD1_1K = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_1K), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_1K)))
            
graphD1_10K = TGraphErrors(len(Diode1_laserstrom), array('d',Diode1_laserstrom) ,array('d',Diode1_U_10K), 
            array('d',[1]*len(Diode1_laserstrom)), array('d',[2]*len(Diode1_U_10K)))


canvasD1 = TCanvas('Diode 1', 'Photo1')
canvasD1.SetGrid()
graphD1_50R.Draw('APX')
graphD1_1K.Draw('SAME')
canvasD1.Update()
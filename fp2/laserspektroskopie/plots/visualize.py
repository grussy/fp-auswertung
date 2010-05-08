#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from math import pi, cos, sin, sqrt, exp
import sys; sys.path.append('/usr/lib/root/')
from messung import Messung
from ROOT import gROOT, TCanvas, TLegend, TF1, TH1F, TGraph, TMultiGraph, TGraphErrors
import os.path

nummer = sys.argv[1]
visu = Messung(nummer, 'Visualisierung von %s' % nummer,0)
visu.plot()
raw_input();
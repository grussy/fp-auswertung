#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Physikalische Konstanten
'''

from math import pi
from Scientific.Physics.PhysicalQuantities import PhysicalQuantity as Q

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

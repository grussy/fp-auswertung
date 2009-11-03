#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import pi

# -------------------------------------------------------------------
# Physikalische Konstanten und angegebene Werte
# -------------------------------------------------------------------

e    = 1.60217733e-19  # Elementarladung [C]
h    = 6.6260755e-34   # Plancksche Konstante [Js]
phi0 = h/(2*e)         # Magnetisches Flussquantum [Vs]
mu0  = 4*pi*1e-7       # Permeabilitaetskonstante [T^2 m^3 J^-1]

Feff = 5e-8       # Effektive Flaeche [m^2]
Ffl  = 9.3e-9	  # Feld-Fluss-Koeffizient [T/phi0]
#r    = 2.9e-3     # Schleifenradius [m]
r    = 3e-3     # Schleifenradius [m]
sr   = 0.5e-3     # Fehler des Schleifenradius [m]
A    = pi*r**2    # Flaeche der Leiterschleife [m^2]
sA   = 2*pi*r*sr  # Fehler der Flaeche der Leiterschleife [m^2]
omega, somega = 0.874103, 0.000433 # Winkelgeschwindigkeit bei Einstellung 10

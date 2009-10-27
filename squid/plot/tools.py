#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import sqrt

def gew_mittel(xsx):
    '''gew_mittel(list(float,float)) -> (float, float)
    xsx  : Liste aus Tupeln der Messwerte mit jeweiligen Fehlern
    ->   Tupel (gx, sgx) aus gewichtetem Mittel und dessen Fehler'''
    suma = sumb = 0.
    for xi,sxi in xsx:
        suma += xi / sxi**2
        sumb += 1. / sxi**2
    return (suma/sumb, 1/sqrt(sumb))

def arith_mittel(x):
    '''arith_mittel(list(float)) -> float
    x  : Liste aus Messwerte
    ->   arithmetisches Mittel der Messwerte'''
    sumx = 0.
    for xi in x:
        sumx += xi
    return sumx / len(x)

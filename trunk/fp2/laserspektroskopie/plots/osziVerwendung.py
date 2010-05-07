#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
import sys; sys.path.append('/usr/lib/root/')
from oszi import OsziData


#######################################################
#
# Zeigt die Verwendung von oszi.py
#
#######################################################


# Oszidata ( String dateinummer XX, String Beschreibung )
test = OsziData('04', 'Dopplerverbreitert Messung 3')
print test.ch1.x[0:12]
print test.ch2.y[13:45]
print test.ch2.yUnits
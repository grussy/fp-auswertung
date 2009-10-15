#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import sqrt, log, pi

# -------------------------------------------------------------------
# Berechnung der Halbwertszeit von Samarium
# -------------------------------------------------------------------


# Messwerte ---------------------------------------------------------

t = 4300.           # Messzeit [s]
n = 0.349           # Zählrate [cps]

tu = 3000.          # Messzeit fuer den Untergrund [s]
u = 0.046           # Untergrundrate [cps]

d = 2.9            # Durchmesser [cm]
F = pi * (d/2.)**2  # Fläche des Präparats [cm**2]


# Messfehler --------------------------------------------------------

sn = sqrt((n+u)/t + u/tu)  # Fehler der Zählrate [s]
sd = 0.01                  # Fehler des Durchmessers [cm]
sF = pi/2 * d * sd         # Fehler der Fläche [cm**2]

print "\nMesswerte:"
print "Messzeit t [s]:    %.0f" % t
print "Zählrate n [1/s]:  %.3f +- %.3f" % (n,sn)
print "Durchmesser d [cm]: %.3f +- %.3f" % (d,sd)
print "Fläche F [cm^2]: %.3f +- %.3f" % (F,sF)


# Näherung von Bragg und Cleeman ------------------------------------

R_luft = 1.13        # Reichweite in Luft [m]
rho_luft = 0.001226  # Luftdichte [g/cm**3]

ma_n  = 14.01        # Atomgewicht [g/mol] von N2
ma_o  = 16.00        # Atomgewicht [g/mol] von O2
ma_ar = 39.95        # Atomgewicht [g/mol] von Ar
ma_sm = 150.36

pl_n  = 0.7551       # Relativer Anteil von N in der Luft
pl_o  = 0.2301       # Relativer Anteil von O in der Luft
pl_ar = 0.0129       # Relativer Anteil von Ar in der Luft

# effektives Atomgewicht von Luft
ma_luft_sqrt = pl_n*sqrt(ma_n) + pl_o*sqrt(ma_o) + pl_ar*sqrt(ma_ar)
ma_luft = ma_luft_sqrt**2

# Relativer Anteil von Sm und O in Samariumoxid
ps_sm  = 2.*ma_sm / (2.*ma_sm + 3.*ma_o)
ps_o   = 3.*ma_o / (2.*ma_sm + 3.*ma_o)

# effektives Atomgewicht von Samariumoxid
ma_smo_sqrt = ps_sm*sqrt(ma_sm) + ps_o*sqrt(ma_o)
ma_smo = ma_smo_sqrt**2

# R * rho von Samariumoxid
R_rho = R_luft * rho_luft * ma_smo_sqrt / ma_luft_sqrt

print "\nNäherung von Bragg und Cleeman:"
print "Effektives Atomgewicht von Luft [g/mol]: %.4f" % ma_luft
print "Effektives Atomgewicht von Samariumoxid [g/mol]: %.4f" % ma_smo
print "R * rho = %.6f" % R_rho


# Berechnung der Halbwertszeit --------------------------------------

na = 6.0221367 * 10**23      # Avogadrozahl

mr_smo = 2.*ma_sm + 3.*ma_o  # Relative Masse von Samariumoxid [g/mol]
h_rel = 0.1487               # Relative Häufigkeit von Sm-147 in Sm

# Die Halbwertszeit
t12 = na * log(2) * R_rho * h_rel * F / (2. * n * mr_smo)
t12a = t12 / 3600. / 24. / 365.

# Fehler der Halbwertszeit
st12 = t12 * sqrt((sn/n)**2 + (sF/F)**2)
st12a = t12a * sqrt((sn/n)**2 + (sF/F)**2)

print "\nBerechnung der Halbwertszeit:"
print "Relative Masse von Samariumoxid [g/mol]: %.2f" % mr_smo
print "Relative Häufigkeit von Sm-147: %.4f" % h_rel
print "Halbwertszeit [s]: %g +- %g" % (t12, st12)
print "Halbwertszeit [a]: %g +- %g" % (t12a, st12a)

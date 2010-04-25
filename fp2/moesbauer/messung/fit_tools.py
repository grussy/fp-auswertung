#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

'''
Fit-Hilfsroutinen
'''

from ROOT import TLegend, TF1


def create_fit_legend(f, fcn_name = 'f(x)', fit_name = 'Fit',
                      show_fstr = True, fstr_nl = True, fstr = [],
                      lpos = (0.59, 0.65, 0.89, 0.88)):
    '''
    Erzeugt eine Legende fuer die uebergebene Fitfunktion.
    f:         Die Fitfunktion
    fcn_name:  Bezeichnung der Fitfunktion
    fit_name:  Bezeichnung des Fits
    show_fstr: Fitfunktion mit ausgeben
    fstr_nle:  Fitfunktion in neuer Zeile ausgeben
    fstr:      Liste zum Ueberschreiben der Funktionsformeldarstellung
    lpos:      Die Position der Legende
    '''
    lg = TLegend(lpos[0], lpos[1], lpos[2], lpos[3])
    lg.SetFillColor(0)
    lg.SetHeader('')
    
    par_count = f.GetNpar()
    if show_fstr and not fstr:
        ft = f.GetTitle()
        for i in range(par_count):
            ft = ft.replace('[%d]' % i, f.GetParName(i))
        if fstr_nl:
            lg.AddEntry(f, '%s: %s' % (fit_name, fcn_name), 'l')
            lg.AddEntry(f, '%s = %s' % (fcn_name, ft), '')
        else:
            lg.AddEntry(f, '%s: %s = %s' % (fit_name, fcn_name, ft), 'l')
    else:
        lg.AddEntry(f, '%s: %s' % (fit_name, fcn_name), 'l')

    if fstr:
        for fstri in fstr:
            lg.AddEntry(f, fstri, '')

    ndf = f.GetNDF()
    if ndf > 0:
        chisq = f.GetChisquare()
        lg.AddEntry(f, '#chi^{2}/ndf = %.2f/%d = %.2f' % (
            chisq, ndf, chisq/ndf), '')

    for i in range(par_count):
        pn, pv, pe = f.GetParName(i), f.GetParameter(i), f.GetParError(i)
        lg.AddEntry(f, '%s = %.4g #pm %.4g' % (pn, pv, pe), '')

    #lg.AddEntry(f, '', '')
    
    return lg


def print_fit_result(f, fcn_name = 'f(x)', show_fstr = True):
    '''
    Gibt ein huebscheres Fit-Ergebnis aus.
    f:         Die Fitfunktion
    fcn_name:  Bezeichnung der Fitfunktion
    show_fstr: Fitfunktion mit ausgeben
    '''
    par_count = f.GetNpar()

    pnames = []
    max_pname_len = 0
    for i in range(par_count):
        pn = f.GetParName(i)
        for c in '#_{}':
            pn = pn.replace(c, '')
        pnames += [pn]
        max_pname_len = max(max_pname_len, len(pn))
        
    if show_fstr:
        ft = f.GetTitle()
        for i in range(par_count):
            ft = ft.replace('[%d]' % i, pnames[i])
        print '%s = %s' % (fcn_name, ft)

    ndf = f.GetNDF()
    if ndf > 0:
        chisq = f.GetChisquare()
        print 'chisq/ndf = %.2f/%d = %.4f' % (chisq, ndf, chisq/ndf)

    ostr = '%' + '%d' % (max_pname_len+1) + 's = %10g +- %g'
    for i in range(par_count):
        pn, pv, pe = pnames[i], f.GetParameter(i), f.GetParError(i)
        print ostr % (pn, pv, pe)


def get_fit_result(f):
    '''
    Liefert ein Dictionary mit den Fitergebnissen.
    f: Die Fitfunktion
    '''
    par_count = f.GetNpar()
    
    pnames = []
    for i in range(par_count):
        pn = f.GetParName(i)
        for c in '#_{}':
            pn = pn.replace(c, '')
        pnames += [pn]

    d = {}
    
    d['ndf'] = f.GetNDF()
    d['chisq'] = f.GetChisquare()
    if d['ndf'] > 0:
        d['rchisq'] = d['chisq'] / d['ndf']

    for i in range(par_count):
        d[pnames[i]] = (f.GetParameter(i), f.GetParError(i))
    
    return d

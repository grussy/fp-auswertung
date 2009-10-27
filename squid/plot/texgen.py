
def table_schleife(ms):
    s = r'''\begin{tabular}{|c|c|c|c|c|c|c|c|c|}
\hline
R & $U_{bat} \, [V]$ & Sens & Mode & Filter & Notch & Geschw & Rot\# & Datei \\ 
\hline '''
    for m in ms:
        #s += '$%d \\, \\Omega$' % m.R
        s += '$%s_{%s}$' % (m.bez[0], m.bez[1])
        s += ' & %.2f' % m.Ubat
        s += ' & $%s$' % m.sens.replace('x', '\\times ')
        s += ' & %s' % m.mode
        s += ' & %s' % m.filt
        s += ' & %s' % m.notch
        s += ' & %s' % m.geschw
        s += ' & $%s$' % m.nrot
        s += ' & \\texttt{%s} \\\\\n' % m.name.replace('_','\\_')
    s += r'''\hline\end{tabular}'''
    return s

def table_gegenstaende(mg):
    s = r'''\begin{tabular}{|c|c|c|c|c|c|c|}
\hline
Gegenstand & Sens & Mode & Filter & Geschw & Rot\# & Datei \\ 
\hline '''
    for m in mg:
        s += m.bez
        s += ' & $%s$' % m.sens.replace('x', '\\times ')
        s += ' & %s' % m.mode
        s += ' & %s' % m.filt
        s += ' & %s' % m.geschw
        s += ' & $%s$' % m.nrot
        s += ' & \\texttt{%s} \\\\\n' % m.name.replace('_','\\_')
    s += r'''\hline\end{tabular}'''
    return s

def table_sinusfit(mf):
    s = r'''\begin{tabular}{|c|c|c|c|c|}
\hline
Datei & $\chi^2 / ndf$ & Offset $a$ [V] & Amplitude $b$ [V] & Phase $c$ [$^{\circ}$] \\ 
\hline '''
    for m in mf:
        if m.fitable:
            s += '\\texttt{%s}' % m.name.replace('_','\\_')
            s += ' & $%.2f / %d$' % (m.chisq, m.ndf)
            s += ' & %.4f $\\pm$ %.4f' % (m.a, m.sa)
            s += ' & %.4f $\\pm$ %.4f' % (m.b, m.sb)
            s += ' & %.4f $\\pm$ %.4f' % (m.c, m.sc)
            s += '\\\\\n'
    s += r'''\hline\end{tabular}'''
    return s

def table_z(mf):
    s = r'''\begin{tabular}{|c|c|c|}
\hline
Datei & $B_z$ [$10^{-9}\,T$] & $z$ [$cm$] \\ 
\hline '''
    for m in mf:
        if m.fitable:
            s += '\\texttt{%s}' % m.name.replace('_','\\_')
            s += ' & %.4f $\\pm$ %.4f' % (m.Bz*1e9, m.sBz*1e9)
            s += ' & %.4f $\\pm$ %.4f' % (m.z*100, m.sz*100)
            s += '\\\\\n'
    s += r'''\hline\end{tabular}'''
    return s

def table_schleife_dipol(mf):
    s = r'''\begin{tabular}{|c|c|c|}
\hline
Datei & $p_{theo}$ [$10^{-7}\,A m^2$] & $p_m$ [$10^{-7}\,A m^2$] \\ 
\hline '''
    for m in mf:
        if m.fitable:
            s += '\\texttt{%s}' % m.name.replace('_','\\_')
            s += ' & %.4f $\\pm$ %.4f' % (m.pt*1e7, m.spt*1e7)
            s += ' & %.4f $\\pm$ %.4f' % (m.pm*1e7, m.spm*1e7)
            s += '\\\\\n'
    s += r'''\hline\end{tabular}'''
    return s

def write_table_schleife(mg):
    f = open('table/schleife.out.tex', 'w')
    f.write(table_gegenstaende(mg))
    f.close()

def write_table_schleife_fit(mg):
    f = open('table/schleife_fit.out.tex', 'w')
    f.write(table_sinusfit(mg))
    f.close()

def write_table_gegenstaende(mg):
    f = open('table/gegenstaende.out.tex', 'w')
    f.write(table_gegenstaende(mg))
    f.close()

def write_table_gegenstaende_fit(mg):
    f = open('table/gegenstaende_fit.out.tex', 'w')
    f.write(table_sinusfit(mg))
    f.close()

def write_table_z(mf):
    f = open('table/z.out.tex', 'w')
    f.write(table_z(mf))
    f.close()

def write_table_schleife_dipol(mf):
    f = open('table/schleife_dipol.out.tex', 'w')
    f.write(table_schleife_dipol(mf))
    f.close()

#Energie eichung des Multikanalanalysators

#Messübersichtdatei (hier stehen die Dateinamen der Datendateien und alle nötigen Einstellungen der jeweiligen Messreihen)
messuebersicht = 'messuebersicht_eichung.dat'

#Klasse Messung (zum auslesen der Messdaten, plotten, fitten)
class Messung:
	#name(string):Dateiname, K_energie(float):Energie des
    def __init__(self, name, K_energie, fitparameter):
        self.name = name
	self.kenergie = K_energie
	self.fitparameter = fitparameter

    

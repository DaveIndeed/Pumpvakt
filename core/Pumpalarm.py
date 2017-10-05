from datetime import datetime, timedelta
from time import sleep
import logging



"""
Godkända tidsenheter: Sekund, Minut, Kvart, Timme, Dygn
De kortaste tidenheterna (sekund, minut) används enbart för enhetstest
"""

class Pumpalarm:
    """Tidhållare / Alarm som håller reda på när saker ska utföras"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tidenheter = {'Sekund':('seconds',1), 'Minut':('seconds', 60),'Kvart':('seconds', 900), 'Timme':('seconds', 3600), 'Dygn':('days', 1)}
        self.senasteLarmtidpunkt = None
        self.nastaLarmtidpunkt = None
    
    def konfigurera(self, tidenhet, tidmangd):
        if tidenhet not in self.tidenheter:
            raise ValueError("Ogiltig tidenhet " + tidenhet)
        if tidenhet != 'Dygn':
            self.antalDeltaSekunder = self.tidenheter[tidenhet][1] * tidmangd
            print("Beställd fördröjning: " + self.antalDeltaSekunder + " sekunder")
            if self.antalDeltaSekunder >= 86399:
                raise ValueError("Ogiltig fördröjning. Fördröjning längre än 24 timmar måste använda enhet Dygn")
        self.tidenhet = tidenhet
        self.tidmangd = tidmangd
    
    def sattNastaLarm(self):
        "Räkna fram tidpunkt för nästa larm"
        
        if self.senasteLarmtidpunkt == None:
            self.senasteLarmtidpunkt = datetime.now()
        #self.nastaLarmtidpunkt = self.senasteLarmtidpunkt + timedelta(second) 
        
    
    def isLarmAktivt(self):
        "Property som signalerar om larm inträffat och inte markerats som hanterat"
        pass
    
    def markeraLarmhanterat(self):
        "Markera att larm har hanterats"
        pass

if __name__ == '__main__':
    p = Pumpalarm()
    p.konfigurera("sekund", 1)
    p.sattNastaLarm()
    if p.isLarmAktivt():
        print("Fel! Larm ska inte ha inträffat än")
    sleep(2)
    if p.isLarmAktivt():
        print("Larm aktivt. Markerar som hanterat")
        p.markeraLarmhanterat()
    else:
        print("Fel! Larm borde ha aktiverats")
    if p.isLarmAktivt():
        print("Fel! Larm borde vara avaktiverat")

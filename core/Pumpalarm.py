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
            if self.antalDeltaSekunder < 1:
                raise ValueError("Ogiltig fördröjning. Måste vara minst en sekund")
            if self.antalDeltaSekunder >= 86399:
                raise ValueError("Ogiltig fördröjning. Fördröjning längre än 24 timmar måste använda enhet Dygn")
        else:
            self.antalDeltaSekunder=0
        self.tidenhet = tidenhet
        self.tidmangd = tidmangd
    
    def sattNastaLarm(self):
        "Räkna fram tidpunkt för nästa larm"
        
        if self.senasteLarmtidpunkt == None:
            self.senasteLarmtidpunkt = datetime.now()
        if self.antalDeltaSekunder > 0:
            self.nastaLarmtidpunkt = self.senasteLarmtidpunkt + timedelta(seconds=self.antalDeltaSekunder)
        else:
            self.nastaLarmtidpunkt = self.senasteLarmtidpunkt + timedelta(days=self.tidmangd)
        
    
    def isLarmAktivt(self):
        "Property som signalerar om larm inträffat och inte markerats som hanterat"
        if (self.nastaLarmtidpunkt != None) and (datetime.now() > self.nastaLarmtidpunkt):
            return True
        else:
            return False
    
    def markeraLarmhanterat(self):
        "Markera att larm har hanterats"
        self.nastaLarmtidpunkt = None


if __name__ == '__main__':
    p = Pumpalarm()
    p.konfigurera("Minut", 1)
    p.sattNastaLarm()
    print("Larm satt till om " + str(p.tidmangd) + " " + p.tidenhet)
    if p.isLarmAktivt():
        print("Fel! Larm ska inte ha inträffat än")
    else:
        print("OK! Larm har inte inträffat ännu")
    print("Väntar så larm ska hinna inträffa")
    sleep(p.antalDeltaSekunder+1)
    if p.isLarmAktivt():
        print("Larm aktivt, OK!")
        print("Markerar att larm har hanterats")
        p.markeraLarmhanterat()
    else:
        print("Fel! Larm borde ha aktiverats")
    if p.isLarmAktivt():
        print("Fel! Larm borde vara avaktiverat")
    else:
        print("OK! Larm är inte aktiverat")
    print("Klart")

from datetime import datetime
from pathlib import Path
import os


class Bildlagring:
    """Funktionalitet för bildlagring"""
    
    def __init__(self):
        self.filformat=".png"
        self.rootmapp = Path("~/bilder")
        
    def getArsmapp(self):
        ar = datetime.now().strftime("%Y")
        return self.rootmapp / ar  
    
    def getManadsmapp(self):
        man = datetime.now().strftime("%m")
        return self.getArsmapp() / man  
        
    def getDagsmapp(self):
        dag = datetime.now().strftime("%d")
        return self.getManadsmapp() / dag  
        
    def getFilkatalog(self):
        """
           Returnera sökväg till katalog att lagra bild
           Om katalogen inte existerar skapas den
        """
        
        path = self.getDagsmapp().expanduser().resolve()
        if not path.exists():
            path.mkdir(parents=True)
        return path
    
    def getTidstampel(self):
        tid = datetime.now().strftime("%Y%m%d_%H%M")
        return tid;
        
    def getFilnamn(self):
        """Returnera filnamn för bild inklusive sökväg"""
        
        filnamn = self.getTidstampel() + self.filformat
        return self.getFilkatalog() / filnamn


if __name__ == '__main__':
        b = Bildlagring()
        print(b.getTidstampel())
        print(b.getFilnamn())

from datetime import datetime
import os


class Bildlagring:
    """Funktionalitet för bildlagring"""
    
    def __init__(self):
        self.filformat=".png"
        self.rootmapp = "~/bilder"
        
    def getArsmapp(self):
        ar = datetime.now().strftime("%Y")
        return os.path.join(self.rootmapp, ar)  
    
    def getManadsmapp(self):
        man = datetime.now().strftime("%m")
        return os.path.join(self.getArsmapp(), man)  
        
    def getDagsmapp(self):
        dag = datetime.now().strftime("%d")
        return os.path.join(self.getManadsmapp(), dag)  
        
    def getFilkatalog(self):
        return self.getDagsmapp()
    
    def getTidstampel(self):
        tid = datetime.now().strftime("%Y%m%d_%H%M")
        return tid;
        
    def getFilnamn(self):
        filnamn = self.getTidstampel() + self.filformat
        return os.path.join(self.getFilkatalog(), filnamn)  


if __name__ == '__main__':
        b = Bildlagring()
        print(b.getTidstampel())
        print(b.getFilnamn())

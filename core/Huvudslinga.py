import logging
#import configparser
from time import sleep
from Pumpalarm import Pumpalarm
from Arduinocomm import Ardiunocomm
from pumpkamera import PumpKamera
from bildlagring import Bildlagring


class Huvudslinga:
    """Huvudslinga för kameran"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.alarm = Pumpalarm()
        self.alarm.konfigurera("Minut", 3)
        self.alarm.sattNastaLarm()
        self.arduino = Ardiunocomm()
        self.kamera = PumpKamera()
        self.bildlagring = Bildlagring() 

    def tandBlixt(self):
        self.arduino.write("led 1 on")
        self.arduino.write("led 2 on")
        self.arduino.write("led 3 on")

    def slackBlixt(self):
        self.arduino.write("led 1 off")
        self.arduino.write("led 2 off")
        self.arduino.write("led 3 off")

    def takort(self):
        self.tandBlixt()
        bild=self.bildlagring.getFilnamn()
        self.kamera.ta_bild(bild)
        self.slackBlixt()

    def aktivitet(self):
        if self.alarm.isLarmAktivt():
            self.takort()
            self.alarm.sattNastaLarm()


# Huvudslinga
if __name__ == '__main__':
    h = Huvudslinga()
    while True:
        h.aktivitet()
        sleep(1)

from time import sleep
from datetime import datetime
from picamera import PiCamera
from fractions import Fraction

def log(message):
	print (datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + message)


resolution_low = (640, 480)
resolution_medel = (1640, 1232)
resolution_hog = (3280, 2464)

zoomfaktor_ingen = (0.0, 0.0 ,1.0, 1.0)
zoomfaktor_lag = (0.2, 0.2, 0.8, 0.8)
zoomfaktor_medel = (0.3, 0.3, 0.7, 0.7)
zoomfaktor_hog = (0.4, 0.4, 0.6, 0.6)

vantetid_lag = 2
vantetid_medel = 10
vantetid_hog = 30

camera = PiCamera()
camera.resolution = resolution_hog
camera.brightness=50
camera.framerate_range = (Fraction(1, 10), Fraction(1))
camera.iso=800
camera.zoom = zoomfaktor_ingen
vantetid = vantetid_medel
#print("Låter kamera mäta ljus")
log("Mät ljus")
camera.start_preview()
sleep(vantetid)
log("Tar bild")
camera.capture('bild.png')
log("Klart")


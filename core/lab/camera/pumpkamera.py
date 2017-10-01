from time import sleep
from picamera import PiCamera
from fractions import Fraction
import logging
import configparser


class Framerate:
	framerate_natt = (Fraction(1, 10), Fraction(1))
	framerate_dag = (Fraction(1, 5), 10)


class Resolution:
	resolution_lag = (640, 480)
	resolution_mellan = (1640, 1232)

class PumpKamera:
	"""Kamerahanering"""


	resolution_hog = (3280, 2464)

	zoomfaktor_ingen = (0.0, 0.0 ,1.0, 1.0)
	zoomfaktor_lag = (0.2, 0.2, 0.6, 0.6)
	zoomfaktor_mellan = (0.3, 0.3, 0.4, 0.4)
	zoomfaktor_hog = (0.4, 0.4, 0.2, 0.2)

	vantetid_kort = 2
	vantetid_mellan = 10
	vantetid_lang = 30

	iso_100 = 100
	iso_200 = 200
	iso_400 = 400
	iso_800 = 800

	camera = PiCamera()

	def __init__(self):
		logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)
		self.camera.resolution = self.resolution_hog
		self.camera.brightness = 50
		self.camera.framerate_range = self.framerate_natt
		self.camera.iso = self.iso_200
		self.camera.zoom = self.zoomfaktor_mellan
		self.vantetid = self.vantetid_mellan
		self.las_settings()

	def las_settings(self):
		config = configparser.RawConfigParser()
		config.read('pumpvakt_setting.ini')
		hastighet = config.get("Kamera", "hastighet")
		self.logger.debug("Tolkat hastighet : " + hastighet)
		upplosning = config.get("Kamera", "upplosning")
		self.logger.debug("Tolkat Upplösning : " + upplosning)
		zoomfaktor = config.get("Kamera", "zoomfaktor")
		self.logger.debug("Tolkat Zoomfaktor : " + zoomfaktor)
		vantetid = config.get("Kamera", "vantetid")
		self.logger.debug("Tolkat väntetid : " + vantetid)
		iso = config.get("Kamera", "iso")
		self.logger.debug("Tolkat iso : " + iso)

	def ta_bild(self, bildfil):
		logger = logging.getLogger(__name__)
		logger.info("Mät ljus")
		self.camera.start_preview()
		sleep(self.vantetid)
		logger.info("Tar bild")
		self.camera.capture(bildfil)
		logger.info("Klart")


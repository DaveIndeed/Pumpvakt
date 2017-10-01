from time import sleep
from picamera import PiCamera
from fractions import Fraction
import logging
import configparser


class CameraSetting:

	logger = logging.getLogger(__name__)
	values = ()
	currentvalue = None
	
	def parse(self, value):
		self.logger.debug("Tolkar värde " + value)
		for i in self.values:
			if value.upper() == i[0].upper():
				self.logger.debug("Hittat match: " + i)
				self.currentvalue=i
		return self.currentvalue[1]


class Framerate(CameraSetting):

	logger = logging.getLogger(__name__)
	natt = ('natt', (Fraction(1, 10), Fraction(1)))
	dag = ('dag', (Fraction(1, 5), 10))
	values = (natt, dag)
	currentvalue=natt
	
# 	def parse(self, value):
# 		for i in self.values:
# 			if value.upper() == i[0].upper():
# 				self.currentvalue=i


class Resolution(CameraSetting):
	
	logger = logging.getLogger(__name__)
	lag = ('lag', (640, 480))
	mellan = ('mellan', (1640, 1232))
	hog = ('hog', (3280, 2464))
	values = (lag, mellan, hog)
	currentvalue=hog[1]

# 	def parse(self, value):
# 		for i in self.values:
# 			if value.upper() == i[0].upper():
# 				self.currentvalue=i


class Zoomfaktor:
	logger = logging.getLogger(__name__)
	ingen = ('ingen', (0.0, 0.0 ,1.0, 1.0))
	lag = ('lag', (0.2, 0.2, 0.6, 0.6))
	mellan = ('mellan', (0.3, 0.3, 0.4, 0.4))
	hog = ('hog', (0.4, 0.4, 0.2, 0.2))
	values = (ingen, lag, mellan, hog)
	currentvalue=mellan

# 	def parse(self, value):
# 		for i in self.values:
# 			if value.upper() == i[0].upper():
# 				self.currentvalue=i


class Vantetid:
	logger = logging.getLogger(__name__)
	kort = ('kort', 2)
	mellan = ('mellan', 10)
	lang = ('lang', 30)
	values = (kort, mellan, lang)
	currentvalue = mellan

# 	def parse(self, value):
# 		for i in self.values:
# 			if value.upper() == i[0].upper():
# 				self.currentvalue=i


class Iso:
	logger = logging.getLogger(__name__)
	iso_100 = ('100', 100)
	iso_200 = ('200', 200)
	iso_400 = ('400', 400)
	iso_800 = ('800', 800)
	values = (iso_100, iso_200, iso_400, iso_800)
	currentvalue = iso_400

# 	def parse(self, value):
# 		self.logger.debug("Tolkar värde " + value)
# 		for i in self.values:
# 			if value.upper() == i[0].upper():
# 				self.logger.debug("Hittat match: " + i)
# 				self.currentvalue=i
# 		return self.currentvalue[1]


class PumpKamera:
	"""Kamerahantering"""


	def __init__(self):
		logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)
		self.camera = PiCamera()
		self.inisektion = "Kamera"
# 		self.camera.resolution = self.resolution_hog
# 		self.camera.brightness = 50
# 		self.camera.framerate_range = self.framerate_natt
# 		self.camera.iso = self.iso_200
# 		self.camera.zoom = self.zoomfaktor_mellan
# 		self.vantetid = self.vantetid_mellan
# 		self.las_settings()


	def las_settings(self):
		config = configparser.RawConfigParser()
		config.read('pumpvakt_setting.ini')
		self.camera.resolution = Resolution().parse(config.get(self.inisektion, "hastighet"))
		self.camera.framerate_range = Framerate().parse(config.get(self.inisektion, "upplosning"))
		self.camera.iso = Iso().parse(config.get(self.inisektion, "iso"))
		self.camera.zoom = Zoomfaktor().parse(config.get(self.inisektion, "zoomfaktor"))
		self.vantetid = Vantetid().parse(config.get(self.inisektion, "vantetid"))
# 		self.logger.debug("Tolkat hastighet : " + hastighet)
# 		upplosning = config.get("Kamera", "upplosning")
# 		self.logger.debug("Tolkat Upplösning : " + upplosning)
# 		zoomfaktor = config.get("Kamera", "zoomfaktor")
# 		self.logger.debug("Tolkat Zoomfaktor : " + zoomfaktor)
# 		vantetid = config.get("Kamera", "vantetid")
# 		self.logger.debug("Tolkat väntetid : " + vantetid)
# 		iso = config.get("Kamera", "iso")
# 		self.logger.debug("Tolkat iso : " + iso)

	def ta_bild(self, bildfil):
		logger = logging.getLogger(__name__)
		logger.info("Mät ljus")
		self.camera.start_preview()
		sleep(self.vantetid)
		logger.info("Tar bild")
		self.camera.capture(bildfil)
		logger.info("Klart")


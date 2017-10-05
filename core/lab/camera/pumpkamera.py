from time import sleep
from picamera import PiCamera
from fractions import Fraction
import logging
import configparser


		
class CameraSetting:
	"""Basklass för dataklasser"""

	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.values = ()
		self.currentvalue = None
	
	def parse(self, value):
		self.logger.debug("Tolkar värde " + value)
		for i in self.values:
			self.logger.debug("Jämför med " + i[0])
			if value.upper() == i[0].upper():
				self.logger.debug("Hittat match: " + str(i))
				self.currentvalue=i
		self.logger.debug("Returnerar " + str(self.currentvalue))
		return self.currentvalue[1]


class Framerate(CameraSetting):
	"""Datacontainer inställningar framerate"""

	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		natt = ('natt', (Fraction(1, 10), Fraction(1)))
		dag = ('dag', (Fraction(1, 5), 10))
		self.values = (natt, dag)
		self.currentvalue=natt
	


class Resolution(CameraSetting):
	"""Datacontainer inställningar upplösning"""

	def __init__(self):	
		self.logger = logging.getLogger(self.__class__.__name__)
		lag = ('lag', (640, 480))
		mellan = ('mellan', (1640, 1232))
		hog = ('hog', (3280, 2464))
		self.values = (lag, mellan, hog)
		self.currentvalue=hog



class Zoomfaktor(CameraSetting):
	"""Datacontainer för digitalzoom"""
	
	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		ingen = ('ingen', (0.0, 0.0 ,1.0, 1.0))
		lag = ('lag', (0.2, 0.2, 0.6, 0.6))
		mellan = ('mellan', (0.3, 0.3, 0.4, 0.4))
		hog = ('hog', (0.4, 0.4, 0.2, 0.2))
		self.values = (ingen, lag, mellan, hog)
		self.currentvalue=mellan



class Vantetid(CameraSetting):
	"""Datacontainer för inställningar väntetid. Väntetid anger hur lång tid kameran får på sig för ljusmätning och inställning av gain m.m."""
	
	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		kort = ('kort', 2)
		mellan = ('mellan', 10)
		lang = ('lang', 30)
		self.values = (kort, mellan, lang)
		self.currentvalue = mellan



class Iso(CameraSetting):
	"""Datacontainer för inställning av ISO"""
	
	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		iso_100 = ('100', 100)
		iso_200 = ('200', 200)
		iso_400 = ('400', 400)
		iso_800 = ('800', 800)
		self.values = (iso_100, iso_200, iso_400, iso_800)
		self.currentvalue = iso_400



class PumpKamera:
	"""Kamerafunktionalitet"""


	def __init__(self):
		logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
		self.logger = logging.getLogger(self.__class__.__name__)
		self.camera = PiCamera()
		self.inisektion = "Kamera"
		self.las_settings()


	def las_settings(self):
		self.logger.debug("Läser konfigurationsfil")
		config = configparser.RawConfigParser()
		config.read('pumpvakt_setting.ini')
		self.camera.resolution = Resolution().parse(config.get(self.inisektion, "upplosning", fallback="hog"))
		self.camera.framerate_range = Framerate().parse(config.get(self.inisektion, "hastighet", fallback="natt"))
		self.camera.iso = Iso().parse(config.get(self.inisektion, "iso", fallback="400"))
		self.camera.zoom = Zoomfaktor().parse(config.get(self.inisektion, "zoomfaktor", fallback="mellan"))
		self.vantetid = Vantetid().parse(config.get(self.inisektion, "vantetid", fallback="mellan"))


	def ta_bild(self, bildfil):
		self.logger.info("Mät ljus")
		self.camera.start_preview()
		sleep(self.vantetid)
		self.logger.info("Tar bild")
		self.camera.capture(bildfil)
		self.logger.info("Klart")


if __name__ == '__main__':
	k = PumpKamera()
	k.ta_bild('bild.png')

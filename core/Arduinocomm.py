import os
import sys
import serial
import logging
from time import sleep


class Ardiunocomm:

	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.debug("Starting, opening serial port");
		allOk=True
		self.serialDevice='/dev/ttyACM0'
		self.serialSpeed=9600
		try:
			self.ser = serial.Serial(self.serialDevice, self.serialSpeed)
		except:
			allOk=False
			print("Cannot open serial port")
			# traceback.print_exc(file=sys.stdout)
		if not allOk:
			sys.exit()
		self.logger.debug("Serial port opened")


	def read(self, timeout=10):

		self.ser.timeout=timeout
		self.logger.debug("Trying to read from serial")
		readstring = self.ser.readline()
		if (readstring == None):
			self.logger.debug("Nothing read")
			return None
		else:
			readable = str(readstring, encoding='utf-8')
			self.logger.debug(readable)
			return readable


	def write(self, message):
		self.logger.debug("Writing to serial")
		self.ser.write(bytes(message, 'utf-8'))

	def tandLed(self, lednr):
		msg = "led {0} on\n".format(lednr)
		self.write(msg)

	def slackLed(self, lednr):
		msg = "led {0} off\n".format(lednr)
		self.write(msg)


def skriv(a, msgout):
	print("Skriver till serieport")
	print(" ---> " + msgout)
	a.write(msgout)

def las(a, timeout=10):
	print("Läser från serieport")
	msgin = a.read(timeout)
	print(" <--- " + msgin)

if __name__ == '__main__':
	print("Öppnar serieport")
	a = Ardiunocomm()
	msgin = las(a)
	skriv(a, "sldfsdjkf")
	msgin = las(a)
	skriv(a, "gettime")
	msgin=las(a)
	skriv(a, "debug")
	skriv(a, "led 2 on")
	#skriv(a, "led {0} on\n".format(1))
	msg=las(a, 1)
	sleep(1)
	skriv(a, "led 2 off")
	#skriv(a, "led {0} off\n".format(1))
	#sleep(1)
	#msgin=las(a, 1)
	#a.tandLed(1)
	#sleep(1)
	#a.slackLed(1)


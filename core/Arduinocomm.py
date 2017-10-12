import sys
import serial
import logging


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

		

if __name__ == '__main__':
	print("Öppnar serieport")
	a = Ardiunocomm()
	print("Läser från serieport")
	msgin = a.read(10)
	print(" <-- " + msgin)
	print("Skriver till serieport")
	msgout = "slfsdkfdjslsdkf";
	print(" --> " + msgout)
	a.write(msgout)
	msgin=a.read()
	print(" <-- " + msgin)
	
import sys
import traceback
import serial
import datetime


def log(message):
	print("%s - %s"%(str(datetime.datetime.now()), message))


log("Starting, opening serial port");
allOk=True
try:
	ser = serial.Serial('/dev/ttyACM0', 9600)
except:
	allOk=False
	print("Cannot open serial port")
	# traceback.print_exc(file=sys.stdout)

if not allOk:
	sys.exit()

log("Serial port opened")
ser.timeout=10
log("Trying to read from serial")
readstring = ser.readline()
if (readstring == None):
	log("Nothing read")
else:
	readable = str(readstring, encoding='utf-8')
	print(readable)
log("Writing to serial")
ser.write(bytes('adadsdsadasd', 'utf-8'))
readstring = ser.readline()
readable = str(readstring, encoding='utf-8')
print(readable)

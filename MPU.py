import smbus
import math

#Register initialization
PWR_M   = 0x6B
DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_EN   = 0x38
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X  = 0x43
GYRO_Y  = 0x45
GYRO_Z  = 0x47
TEMP = 0x41

bus = smbus.SMBus(1) #maybe 1 if revision 2 boards
address = 0x68

AxCal=0
AyCal=0
AzCal=0
GxCal=0
GyCal=0
GzCal=0

def InitMPU():
	bus.write_byte_data(address, DIV, 7)
	bus.write_byte_data(address, PWR_M, 1)
	bus.write_byte_data(address, CONFIG, 0)
	bus.write_byte_data(address, GYRO_CONFIG, 24)
	bus.write_byte_data(address, INT_EN, 1)
	time.sleep(1)


def calibrate():
	clear()
	Print("Calibrate....")
	global AxCal
	global AyCal
	global AzCal
	x=0
	y=0
	z=0
	for i in range(50):
		x = x + readMPU(ACCEL_X)
		y = y + readMPU(ACCEL_Y)
		z = z + readMPU(ACCEL_Z)
	x= x/50
	y= y/50
	z= z/50
	AxCal = x/16384.0
	AyCal = y/16384.0
	AzCal = z/16384.0

	print(AxCal)
	print(AyCal)
	print(AzCal)

	global GxCal
	global GyCal
	global GzCal
	x=0
	y=0
	z=0
	for i in range(50):
		x = x + readMPU(GYRO_X)
		y = y + readMPU(GYRO_Y)
		z = z + readMPU(GYRO_Z)
	x= x/50
	y= y/50
	z= z/50
	GxCal = x/131.0
	GyCal = y/131.0
	GzCal = z/131.0

	print(GxCal)
	print(GyCal)
	print(GzCal)
 
 

def readMPU(addr):
	high = bus.read_byte_data(address, addr)
	low = bus.read_byte_data(address, addr+1)
	value = ((high << 8) | low)
	if(value > 32768):
		value = value - 65536
	return value

def accel():
	x = readMPU(ACCEL_X)
	y = readMPU(ACCEL_Y)
	z = readMPU(ACCEL_Z)
	Ax = (x/16384.0-AxCal)
	Ay = (y/16384.0-AyCal)
	Az = (z/16384.0-AzCal)
	#print "X="+str(Ax)
	print(Ax,Ay,Az)
	time.sleep(.01)
    
def gyro():
	global GxCal
	global GyCal
	global GzCal
	x = readMPU(GYRO_X)
	y = readMPU(GYRO_Y)
	z = readMPU(GYRO_Z)
	Gx = x/131.0 - GxCal
	Gy = y/131.0 - GyCal
	Gz = z/131.0 - GzCal
	#print "X="+str(Gx)
	print(Gx,Gy,Gz)
	time.sleep(.01)

def temp():
	tempRow=readMPU(TEMP)
	tempC=(tempRow / 340.0) + 36.53
	tempC="%.2f" %tempC
	print(tempC)
	Print("Temp: ")
	Print(str(tempC))
	time.sleep(.2)


def MPU():
	InitMPU()
	calibrate()
	InitMPU()
	for i in range(20):
		temp()
	time.sleep(1)
	for i in range(30):
		accel()
	time.sleep(1)
	for i in range(30):
		gyro()






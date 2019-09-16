import smbus
import math

power_mgmt1 = 0x6b
power_mgmt2 = 0x6c
bus = smbus.SMBus(1) #maybe 1 if revision 2 boards
address = 0x68	



def read_byte(adr):
	return bus.read_byte_data(address, adr)

def read_word(adr):
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr+1)
	val = (high << 8) + low
	return val

def read_word_2c(adr):
	val = read_word(adr)
	if (val >= 0x8000):
		return -((65535-val) + 1)
	else:
		return val

def dist(a,b):
	return math.sqrt((a*a) + (b*b))

def get_x_rotation(x,y,z):
	radians = math.atan2(x, dist(y,z))
	return -math.degrees(radians)

def get_y_rotation(x,y,z):
	radians = math.atan2(y, dist(x,z))
	return math.degrees(radians)




def gyro():

	bus.write_byte_data(address, power_mgmt1, 0)
	print("gyro data")
	print("---------")
	
	gyroX = read_word_2c(0x43)
	gyroY = read_word_2c(0x45)
	gyroZ = read_word_2c(0x47)
	
	print ("Gyro X: ", gyroX, " scaled: ", (gyroX/131))
	print ("Gyro X: ", gyroY, " scaled: ", (gyroY/131))
	print ("Gyro X: ", gyroZ, " scaled: ", (gyroZ/131))
	return(gyroX, gyroY, gyroZ)
	
def acc():
	bus.write_byte_data(address, power_mgmt1, 0)
	print()
	print("accelerometer data")
	print("------------------")
	
	accelX = read_word_2c(0x3b)
	accelY = read_word_2c(0x3d)
	accelZ = read_word_2c(0x3f)
	
	xScaled = accelX/16834.0
	yScaled = accelY/16834.0
	zScaled = accelZ/16834.0
	
	print("X: ", accelX, " scaled: ", xScaled)
	print("Y: ", accelY, " scaled: ", yScaled)
	print("Z: ", accelZ, " scaled: ", zScaled)
	
	return('{0: .3g}'.format(xScaled), '{0: .3g}'.format(yScaled), '{0: .3g}'.format(zScaled))
	
def rotation():
	bus.write_byte_data(address, power_mgmt1, 0)
	accelX = read_word_2c(0x3b)
	accelY = read_word_2c(0x3d)
	accelZ = read_word_2c(0x3f)
	
	xScaled = accelX/16834.0
	yScaled = accelY/16834.0
	zScaled = accelZ/16834.0
	xRot = get_x_rotation(xScaled, yScaled, zScaled)
	yRot = get_y_rotation(xScaled, yScaled, zScaled)
	

	return ('{0: .3g}'.format(xRot), '{0: .3g}'.format(yRot))

#from PCF8574 import PCF8574_GPIO
#from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep, strftime
import subprocess
import re
import board
import adafruit_dht
from datetime import datetime
import csv
import os
#import threading
import smbus2
import adafruit_ltr390
import busio


dhtDevice = adafruit_dht.DHT22(board.D10) #PIN 10 (Data)

#Create Folder with Date Information
now = datetime.now()
readings_dir = os.path.join(os.path.dirname(__file__),"Readings")
folder_name = now.strftime("%m_%d_%y")
folder_path = os.path.join(readings_dir, folder_name)
os.makedirs(folder_path, exist_ok=True)


#Create CSV File with Hourly Information
csv_filename = now.strftime("%H:%M.csv")
csv_path = os.path.join(folder_path, csv_filename)


def get_cpu_temp():
	tmp = open('/sys/class/thermal/thermal_zone0/temp')
	cpu = tmp.read()
	tmp.close()
	return '$:{:.1f}'.format(float(cpu)/1000) + 'C'

def get_time():
	current_datetime = datetime.now()
	return current_datetime.strftime(' %H:%M:%S')

def get_Ambient():
	humidity = dhtDevice.humidity
	temperature = dhtDevice.temperature * (9/5) + 32

	if humidity is not None or temperature is not None:
		return "T:{0:0.1f}F H:{1:0.1f}%".format(temperature, humidity)
	else:
		return 'Sensor Error'

def clean_str(str):
	return re.sub(r'^.{2}|.$','', str)

def loop():
	#mcp.output(3,1)
	#lcd.begin(16,2)

	with open(csv_path, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Time', 'Temperature (F)', 'Humidity', 'UV', 'Ultraviolet Radiation Index', 'Ambient Light', 'Lux', 'CPU'])

		while(True):
			cpu_temp = get_cpu_temp()
			ambient = get_Ambient()
			time = get_time()
			temperature = ambient.split(' ', 1)[0]
			humidity = ambient.split(' ', 1)[1]
			#lcd.setCursor(0,0)  # set cursor position
			#lcd.message(ambient)
			#lcd.message('\n') #Go to Next Line
			#lcd.message(cpu_temp)
			#lcd.message(time)
			writer.writerow([time, clean_str(temperature), clean_str(humidity), ltr.uvs , ltr.uvi , ltr.light , ltr.lux, clean_str(cpu_temp)])
			file.flush()
			sleep(2)

#def destroy():
	#lcd.clear()

#PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
#PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.


# Create PCF8574 GPIO adapter.
#try:
	#mcp = PCF8574_GPIO(PCF8574_address)
#except:
	#try:
		#mcp = PCF8574_GPIO(PCF8574A_address)
	#except:
		#print ('I2C Address Error !')
		#exit(1)

# Create LCD, passing in MCP GPIO adapter.
#lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)


i2c = board.I2C()
ltr = adafruit_ltr390.LTR390(i2c)


if __name__ == '__main__':
	try:
		loop()
	except KeyboardInterrupt:
		#destroy()
		print('exit')

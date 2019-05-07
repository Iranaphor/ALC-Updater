import os
import time
import datetime
import ftplib

#Create log file
f = open("/home/pi/ALC/camera/log.txt", "a")
f.write("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\r\n")
f.close()

#Initiate connection to server
print('delay to ensure internet is active')
session = ftplib.FTP('s1.yourthought.co.uk', 'james-rpi', 'james25', timeout=None)


#varialble used to ensure only 1 picture taken per minute
errorHad = False

os.system("sudo usermod -a -G video pi")
os.system("sudo modprobe uvcvideo")
os.system("sudo rmmod uvcvideo")
os.system("sudo modprobe uvcvideo")
os.system("v4l2-ctl -c sharpness=1 -c exposure_auto=1 -c exposure_absolute=10")

while True:

	#Take Snapshot ActiveCam
	os.system("sudo fswebcam --no-banner -r 5120x3840 /home/pi/ALC/camera/frame.jpeg")
	
	#Taks Snapshot MS USB Webcam
	#os.system("sudo fswebcam --set contrast=1 --set saturation=100 -r 1280x720 --no-banner --crop 1280x570,0x150 /home/pi/ALC/camera/frame.jpeg")
	
	try:
		#Pause
		time.sleep(1)
		
		#Upload Image
		file = open('/home/pi/ALC/camera/frame.jpeg', 'rb')
		session.storbinary('STOR frame.jpeg', file)
		file.close()
		
		#Pause to allow log upload
		time.sleep(1)

		#Write to log
		f = open("/home/pi/ALC/camera/log.txt", "a")
		f.write("[" + str(datetime.datetime.now()) + "] - Frame Generated\r\n")
		f.close()

		#Upload log
		file = open('/home/pi/ALC/camera/log.txt', 'rb')
		session.storbinary('STOR log.txt', file)
		file.close()
		
		#Pause to allow log upload
		time.sleep(1)

		#Update log
		#os.system("sudo fswebcam --no-banner -r 5120x3840 /home/pi/FTP/frame.png")
		f = open("/home/pi/ALC/camera/log.txt", "a")
		f.write("[" + str(datetime.datetime.now()) + "] - Frame Uploaded\r\n")
		f.close()

	except ftplib.error_temp:

		errorHad = True

		f = open("/home/pi/ALC/camera/errlog.txt", "a")
		f.write("[" + str(datetime.datetime.now()) + "] - Frame Upload Failed\r\n")
		f.close()
		

	except session.all_error:

		errorHad = True

		f = open("/home/pi/ALC/camera/errlog.txt", "a")
		f.write("[" + str(datetime.datetime.now()) + "] - Session Error\r\n")
		f.close()
		

session.quit()

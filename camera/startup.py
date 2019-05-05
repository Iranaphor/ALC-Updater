import os
import time
import datetime
import ftplib

#Create log file
f = open("/home/pi/ALC/camera/log.txt", "a")
f.write("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\r\n")
f.close()

#Initiate connection to server
time.sleep(10)
session = ftplib.FTP('s1.yourthought.co.uk', 'james-rpi', 'james25', timeout=None)
time.sleep(15)

#varialble used to ensure only 1 pictre taken per minute
errorHad = False

while True:

	#Take snapshot
	os.system("sudo fswebcam --no-banner -r 5120x3840 /home/pi/ALC/camera/frame.jpeg")

	try:
		#Pause for 54 seconds once first image has been taken
		if errorHad == False:
			time.sleep(24)
		errorHad = False



        	time.sleep(1)
		print("LBL1")

		f = open("/home/pi/ALC/camera/log.txt", "a")
		f.write("[" + str(datetime.datetime.now()) + "] - Frame Generated\r\n")
		f.close()

		time.sleep(1)
		print("LBL2")

		file = open('/home/pi/ALC/camera/log.txt', 'rb')
		session.storbinary('STOR log.txt', file)
		file.close()

		time.sleep(1)
		print("LBL3")

		file = open('/home/pi/ALC/camera/frame.jpeg', 'rb')
		session.storbinary('STOR frame.jpeg', file)
		file.close()

		time.sleep(1)

		#os.system("sudo fswebcam --no-banner -r 5120x3840 /home/pi/FTP/frame.png")
		f = open("/home/pi/ALC/camera/log.txt", "a")
		f.write("[" + str(datetime.datetime.now()) + "] - Frame Uploaded\r\n")
		f.close()

	except ftplib.error_temp:

		errorHad = True
		print("RETRY")

		f = open("/home/pi/ALC/camera/errlog.txt", "a")
		f.write("[" + str(datetime.datetime.now()) + "] - Frame Uploaded\r\n")
		f.close()

session.quit()

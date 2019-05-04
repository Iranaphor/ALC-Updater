import os
import time
import datetime
import ftplib
    
f = open("/home/pi/FTP/log.txt", "a")
f.write("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\r\n")
f.close()

time.sleep(10)

session = ftplib.FTP('s1.yourthought.co.uk', 'james-rpi', 'james25', timeout=None)

time.sleep(15)

errorHad = False
    
while True:
    
    os.system("sudo fswebcam --no-banner -r 5120x3840 /home/pi/FTP/frame.jpeg")
        
    try: 
        
        if errorHad == False:
            time.sleep(54)
        errorHad = False
        
        
        
        time.sleep(1)
        print("LBL1")
        
        f = open("/home/pi/FTP/log.txt", "a")
        f.write("[" + str(datetime.datetime.now()) + "] - Frame Written\r\n")
        f.close()
        
        time.sleep(1)
        print("LBL2")

        file = open('/home/pi/FTP/log.txt', 'rb')
        session.storbinary('STOR log.txt', file)
        file.close()
        
        time.sleep(1)
        print("LBL3")
        
        file = open('/home/pi/FTP/frame.jpeg', 'rb')
        session.storbinary('STOR frame.jpeg', file)
        file.close()
        
        time.sleep(1)
        
        #os.system("sudo fswebcam --no-banner -r 5120x3840 /home/pi/FTP/frame.png")
        f = open("/home/pi/FTP/log.txt", "a")
        f.write("[" + str(datetime.datetime.now()) + "] - Frame Uploaded\r\n")
        f.close()

    except ftplib.error_temp:
         
        errorHad = True
        print("RETRY")
        
        f = open("/home/pi/FTP/errlog.txt", "a")
        f.write("[" + str(datetime.datetime.now()) + "] - Frame Uploaded\r\n")
        f.close()
        
session.quit()

#!/bin/bash
cd /home/pi
typ=$(head -n 1 /home/pi/ALC/component)

#Move to ALC-Updater and pull any updates
cd /home/pi/ALC-Updater
if (git pull | grep "Already up-to-date.")
then
	echo "PULL SUCCESSFUL - No change"
	
	echo "STARTING SYSTEM"
	python /home/pi/ALC/$typ/startup.py
	
else
	echo "PULL SUCCESSFUL - Updates found"
	
	#Copy system files and new startup script
	if [ ! -d /home/pi/ALC/$typ ]
        then
                mkdir /home/pi/ALC/$typ
        fi
	cp -r /home/pi/ALC-Updater/$typ/. /home/pi/ALC/$typ/
	cp /home/pi/ALC-Updater/update.sh /home/pi/ALC/update.sh

	#Update autostart and wifi list
	cp /home/pi/ALC/camera/system_files/autostart /etc/xdg/lxsession/LXDE-pi/autostart
	cp /home/pi/ALC/camera/system_files/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

	#reboot
	echo "reeboot"
fi

#!/bin/bash
typ=$(head -n 1 ./ALC/component)

#Move to ALC-Updater and pull any updates
cd ./ALC-Updater
if (git pull | grep "Already up-to-date.")
then
	echo "PULL SUCCESSFUL - No change"
	
	echo "STARTING SYSTEM"
	python ./ACL/$typ/startup.py
	
else
	echo "PULL SUCCESSFUL - Updates found"
	
	#Copy system files and new startup script
	mkdir ./ALC/$typ
	cp -r ./ALC-Updater/$typ/. ./ALC/$typ/
	cp ./ALC-Updater/startup.sh ./ALC/startup.sh

	#Update autostart and wifi list
	cp ./ALC/camera/system_files/autostart ./.config/lxsession/LXDE-pi/autostart
	cp ./ALC/camera/system_files/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

	#reboot
	echo "reeboot"
fi

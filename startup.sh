#!/bin/bash
typ=$(head -n 1 ./ALC/component)
echo "--------"
echo $typ
echo "--------"
updates=false
#Clone latest updates
if [ ! -d ./ALC-Updater ]
then

	echo "NO ALC-UPDATER"
	git clone -b $typ --single-branch https://github.com/Iranaphor/ALC-Updater.git
	updates=true

else
	echo "UPDATE ALC-UPDATER"
	#Move to ALC-Updater and pull any updates
	cd ./ALC-Updater

	if (git pull | grep "Already up-to-date.")
	then
		echo "PULL SUCCESSFUL"
		updates=false
	else
		updates=true
	fi
fi

#Run files or restart device
if $updates
then
	echo "COPYING NEW FILES"
	#Copy system files and new startup script
	mkdir ./ALC/$typ
	cp -r ./ALC-Updater/$typ/. ./ALC/$typ/
	cp ./ALC-Updater/startup.sh ./ALC/startup.sh

	#Update autostart and wifi list
	cp ./ALC/camera/system_files/autostart ./.config/lxsession/LXDE-pi/autostart
	cp ./ALC/camera/system_files/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

	#reboot
else
	echo "STARTING SYSTEM"
	python ./ACL/$typ/startup.py
fi

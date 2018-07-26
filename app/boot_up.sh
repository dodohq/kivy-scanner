#!/bin/bash

systemctl stop gpsd.socket
systemctl disable gpsd.socket
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
chmod 777 /dev/input/event7
kill $(ps aux | grep 'ffmpeg' | awk '(print $2)')
python3 /home/nvidia/scanner_gui/app/main.py



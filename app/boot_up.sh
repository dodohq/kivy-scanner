#!/bin/bash

systemctl stop gpsd.socket
systemctl disable gpsd.socket
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
python3 /home/nvidia/Desktop/scanner_gui/app/init_gpio.py
chmod 777 /dev/input/event7
python3 /home/nvidia/Desktop/scanner_gui/app/main.py



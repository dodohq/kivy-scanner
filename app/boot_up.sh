#!/bin/bash
python3 /home/nvidia/Desktop/scanner_gui/app/init_gpio.py
chmod 777 /dev/input/event7
python3 /home/nvidia/Desktop/scanner_gui/app/main.py



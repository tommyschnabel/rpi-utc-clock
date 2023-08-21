#!/bin/bash

sudo mkdir /etc/rpi-utc-clock
sudo cp ./clock.py /etc/rpi-utc-clock
sudo cp ./Roboto-Medium.ttf /etc/rpi-utc-clock

sudo cp ./utc-clock.service /etc/systemd/system/
sudo systemctl enable utc-clock.service
sudo systemctl start utc-clock.service

#!/bin/bash

mkdir /etc/rpi-utc-clock
cp ./clock.py /etc/rpi-utc-clock
cp ./Roboto-Medium.ttf /etc/rpi-utc-clock

cp ./utc-clock.service /etc/systemd/system/
sudo systemctl enable utc-clock.service
sudo systemctl start utc-clock.service

#!/bin/bash

mkdir /etc/rpi-utc-clock
cp ./clock.py /etc/rpi-utc-clock

cp ./eink-clock.service /etc/systemd/system/
sudo systemctl enable eink-clock.service
sudo systemctl start eink-clock.service

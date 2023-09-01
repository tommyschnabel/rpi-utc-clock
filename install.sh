#!/bin/bash

LOCAL=$1
ALT=$2

INSTALL_DIR=/etc/rpi-utc-clock

if [ "$LOCAL" != "" ]; then
    sudo bash -c "echo $LOCAL > $INSTALL_DIR/local"
    sudo bash -c "echo $ALT > $INSTALL_DIR/alt"
fi

sudo mkdir -p $INSTALL_DIR
sudo cp ./clock.py $INSTALL_DIR
sudo cp ./Roboto-Medium.ttf $INSTALL_DIR

sudo cp ./utc-clock.service /etc/systemd/system/
sudo systemctl enable utc-clock.service
sudo systemctl start utc-clock.service

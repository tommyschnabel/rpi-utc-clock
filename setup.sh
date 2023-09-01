#!/bin/bash

# Parse args
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -h|--help)
        echo "Usage:"
        echo "$0 --local US/Eastern --alt US/Pacific"
        exit 0
        ;;
        --local)
        LOCAL=$2
        shift # Shift past argument
        shift # Shift past value
        ;;
        --alt)
        ALT="$2"
        shift # Shift past argument
        shift # Shift past value
        ;;
    esac
done

wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz
cd bcm2835-1.71/ || exit 1
sudo ./configure && sudo make && sudo make check && sudo make install

# Install python and other tools
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-pil python3-numpy git vim p7zip-full

# Install wiringpi
git clone https://github.com/WiringPi/WiringPi
cd WiringPi || exit 2
./build
gpio -v
cd ..

# Install python packages
sudo pip3 install RPi.GPIO spidev waveshare-epaper pytz

# Install waveshare e-paper modules
wget  https://www.waveshare.com/w/upload/3/39/E-Paper_code.7z
7z x E-Paper_code.7z -O./e-Paper
cd e-Paper/RaspberryPi_JetsonNano/c || exit 3
sudo make clean
sudo make -j4 EPD=epd1in02d
cd - || exit 4

git clone https://github.com/tommyschnabel/rpi-utc-clock.git
cd rpi-utc-clock || exit 5
chmod +x install.sh
sudo ./install.sh "$LOCAL" "$ALT"

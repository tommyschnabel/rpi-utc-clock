# README #

A simple Local (24-hour) and UTC datetime clock, because I can never tell what UTC time means when I'm reading logs.

![utc-clock](./images/utc-clock.jpg)
Runs on a Raspberry Pi with a Waveshare e-ink screen.


![utc-clock](./images/utc-clock-vertical.jpg)
Vertical layout for three clock view.

## Picking out your screen ##
I recommend getting a Waveshare e-paper HAT that screws right into your Pi, otherwise you'll have to use the guide for your screen to plug individual connectors into GPIO pins.

I got the 2.7inch e-Paper HAT, some tweaking might be needed for other boards.

## Installation ##

### Hardware ###
Connect the screen to your raspberry pi as instructed.

### Raspberry Pi OS ###
1. Download and install the [raspberry pi imager](https://www.raspberrypi.com/software/).
1. Install the appropriate 32/64-bit OS on your microSD card.
   1. Lite versions are ok to use
   1. I don't know why, but the Raspberry OS Imager Wi-Fi credentials never set properly for me, so I ended up doing it manually, step is below. All other Imager configs worked as expected.
1. Mount your SD card again. In config.txt uncomment `dtparam=spi=on`
1. Fill out `conf/wpa_supplicant.conf` with your Wi-Fi credentials
1. Copy the files in `./conf/` onto your SD card in its root
1. Insert your SD card into your pi and start it up (it might take a couple of minutes before your Pi connects to Wi-Fi)
1. `scp` the setup.sh file to your Pi, and run it. If you want to set the local timezone or a third alternate timezone, use the following flags (both optional):
   1. `./setup.sh  --local US/Eastern --alt US/Pacific # Both flags optional`
   1. `setup.sh` installs all dependencies and sets up the clock as a service via systemctl (`utc-clock.service`).

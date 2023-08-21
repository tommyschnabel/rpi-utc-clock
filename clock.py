#!/usr/bin/python
import logging
import time
from datetime import datetime, timezone

import epaper
from PIL import Image, ImageDraw, ImageFont

module = 'epd2in7_V2'  # Change this to match the screen you have
screen_height_pixels = 176
screen_width_pixels = 264

screen = epaper.epaper(module)
font_file = '/home/pi/Roboto-Medium.ttf'
time_font_size = 60
label_font_size = 20
date_font_size = 16
logging.basicConfig(level=logging.INFO)  # Note: DEBUG shows screen logs


def local_time():
    return time.strftime('%H:%M')


def local_date():
    return time.strftime("%m/%d/%y")


def utc_time():
    return datetime.now(timezone.utc).strftime('%H:%M')


def utc_date():
    return datetime.now(timezone.utc).strftime("%m/%d/%y")


try:
    logging.info(f"{module} - clock.py")
    epd = screen.EPD()

    # Layout positions and sizes, based on font sizes above
    left_padding = 10
    local_time_start = label_font_size
    local_time_end = local_time_start + time_font_size
    time_width = screen_width_pixels * 0.6
    time_height = time_font_size
    label_height = label_font_size
    utc_label_start = local_time_end + 10
    utc_label_end = utc_label_start + label_font_size
    utc_time_start = utc_label_end
    utc_time_end = utc_time_start + time_font_size
    date_start_x = time_width + 30
    local_date_start_y = local_time_start + time_font_size - date_font_size
    utc_date_start_y = utc_time_start + time_font_size - date_font_size
    params = {
        'screen_width_pixels': screen_width_pixels,
        'screen_height_pixels': screen_height_pixels,
        'left_padding': left_padding,
        'local_time_start': local_time_start,
        'local_time_end': local_time_end,
        'time_width': time_width,
        'time_height': time_height,
        'utc_label_start': utc_label_start,
        'utc_label_end': utc_label_end,
        'utc_time_start': utc_time_start,
        'utc_time_end': utc_time_end,
    }
    logging.info(f'Layout positions/sizes: {params}')

    # Warn on too many unused pixels
    unused_pixels = screen_height_pixels - utc_time_end
    if unused_pixels > 20:
        logging.warning(f'There are {unused_pixels} unused vertical pixels. You can adjust your fonts bigger')

    # Init
    epd.init()
    font = ImageFont.truetype(font_file, time_font_size)
    label_font = ImageFont.truetype(font_file, label_font_size)
    date_font = ImageFont.truetype(font_file, date_font_size)

    # Clear screen
    img = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(img)

    first = True
    while True:
        local = local_time()
        utc = utc_time()
        logging.info(f'Setting time to: local={local}, utc={utc}')

        # Draw labels
        draw.text((left_padding, 0), 'Local Time', font=label_font, fill=0)
        draw.text((left_padding, utc_label_start), 'UTC Time', font=label_font, fill=0)

        # Draw times
        draw.text((left_padding, local_time_start), local, font=font, fill=0)
        draw.text((left_padding, utc_time_start), utc, font=font, fill=0)

        # Draw dates
        draw.text((date_start_x, local_date_start_y), local_date(), font=date_font, fill=0)
        draw.text((date_start_x, utc_date_start_y), utc_date(), font=date_font, fill=0)

        # Update screen
        epd.display_Base(epd.getbuffer(img))

        time.sleep(60)

except IOError as e:
    logging.error(e)
    raise e

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    screen.epdconfig.module_exit()
    exit()

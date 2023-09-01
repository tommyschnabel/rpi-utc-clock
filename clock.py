#!/usr/bin/python
import logging
import time
import os
from datetime import datetime, timezone

import epaper
from PIL import Image, ImageDraw, ImageFont
from pytz import timezone as pytz_timezone

module = 'epd2in7_V2'  # Change this to match the screen you have
screen_height_pixels = 176
screen_width_pixels = 264
screen = epaper.epaper(module)
font_file = '/home/pi/Roboto-Medium.ttf'
logging.basicConfig(level=logging.INFO)  # Note: DEBUG shows screen logs

# Default timezones
local_timezone = datetime.now().astimezone().tzinfo
alt_timezone = None

# Load configured local timezone
cwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file_path = f'{cwd}/local'
if os.path.exists(file_path):
    with open(file_path) as f:
        local_timezone = pytz_timezone(f.read().strip())

# Load configured alt timezone
file_path = f'{cwd}/alt'
if os.path.exists(file_path):
    with open(file_path) as f:
        alt_timezone = pytz_timezone(f.read().strip())

logging.info(f'Using: local={local_timezone}, alt={alt_timezone}')

# Two time clock (no alt time)
if alt_timezone is None:
    time_font_size = 60
    label_font_size = 20
    date_font_size = 16
    time_width = screen_width_pixels * 0.6
    left_padding = 10
else:
    time_font_size = 40
    label_font_size = 12
    date_font_size = 12
    time_width = screen_width_pixels * 0.5
    left_padding = 35


def local_time():
    return datetime.now(local_timezone).strftime('%H:%M')


def local_date():
    return datetime.now(local_timezone).strftime("%m/%d/%y")


def alt_time():
    if alt_timezone is None:
        return ""
    return datetime.now(alt_timezone).strftime('%H:%M')


def alt_date():
    if alt_timezone is None:
        return ""
    return datetime.now(alt_timezone).strftime("%m/%d/%y")


def utc_time():
    return datetime.now(timezone.utc).strftime('%H:%M')


def utc_date():
    return datetime.now(timezone.utc).strftime("%m/%d/%y")


try:
    logging.info(f"{module} - clock.py")
    epd = screen.EPD()

    # Layout positions and sizes, based on font sizes above
    local_time_start = label_font_size
    local_time_end = local_time_start + time_font_size
    time_height = time_font_size
    label_height = label_font_size
    utc_label_start = local_time_end + 10
    utc_label_end = utc_label_start + label_font_size
    utc_time_start = utc_label_end
    utc_time_end = utc_time_start + time_font_size
    date_start_x = time_width + 30
    local_date_start_y = local_time_start + time_font_size - date_font_size
    utc_date_start_y = utc_time_start + time_font_size - date_font_size
    alt_label_start = utc_time_start + time_height + 10
    alt_label_end = alt_label_start + label_font_size
    alt_time_start = alt_label_end
    alt_time_end = alt_time_start + time_font_size
    atl_date_start_y = alt_time_start + time_font_size - date_font_size

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

    while True:
        local = local_time()
        utc = utc_time()
        alt = alt_time()
        alt_log = ""
        if alt != "":
            alt_log = f', alt={alt}'
        logging.info(f'Setting time to: local={local}, utc={utc}{alt_log}')

        # Clear screen
        img = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(img)

        # Draw labels
        draw.text((left_padding, 0), 'Local Time', font=label_font, fill=0)
        draw.text((left_padding, utc_label_start), 'UTC Time', font=label_font, fill=0)

        # Draw times
        draw.text((left_padding, local_time_start), local, font=font, fill=0)
        draw.text((left_padding, utc_time_start), utc, font=font, fill=0)

        # Draw dates
        draw.text((date_start_x, local_date_start_y), local_date(), font=date_font, fill=0)
        draw.text((date_start_x, utc_date_start_y), utc_date(), font=date_font, fill=0)

        # Draw alt timezone
        if alt_timezone is not None:
            draw.text((left_padding, alt_label_start), f'{alt_timezone} Time', font=label_font, fill=0)
            draw.text((left_padding, alt_time_start), alt, font=font, fill=0)
            draw.text((date_start_x, atl_date_start_y), alt_date(), font=date_font, fill=0)

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

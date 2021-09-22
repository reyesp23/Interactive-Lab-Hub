import time
import math
from time import strftime, sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
font_r = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
seconds = 60
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    # Calculate time dilation
    c = 300000 #Speed of light
    r = 0.9 #Ratio
    v = r*c #Traveler speed
    t_dil = 1 / math.sqrt((1-v**2/c**2)) #Time dilation
    text = str(r*100) + "% c"
    
    # Display countdown
    y_label = top + (height - font.getsize(str(seconds))[1]) / 2 + 35
    x_label = 0 + (width - font.getsize(str(seconds))[0]) / 2
    draw.text((x_label,y_label), str(seconds), font=font, fill="#FFFFFF")
    
    # Display speed
    draw.text((width-font_r.getsize(text)[0]-10, bottom-30), text, font=font_r, fill="#888888")

    
    tick = "."
    
    if seconds > 0:
        x_bar = 10
        y_bar = -10
        for i in range(seconds):
            if i > 19: break
            x_bar += font.getsize(tick)[0]
            draw.text((x_bar, y_bar), tick, font = font, fill = "#00ffff")
   
    if seconds > 20:  
        x_bar = 10
        y_bar += font.getsize(tick)[1]
        for i in range(seconds - 20):
            if i > 19: break
            x_bar += font.getsize(tick)[0]
            draw.text((x_bar, y_bar), tick, font = font, fill = "#00ffff")
            
    if seconds > 40:  
        x_bar = 10 
        y_bar += font.getsize(tick)[1]
        for i in range(seconds - 40):
            if i > 19: break
            x_bar += font.getsize(tick)[0]
            draw.text((x_bar, y_bar), tick, font = font, fill = "#00ffff")
    
    # Display image.
    disp.image(image, rotation)
    
    #Counter
    if seconds > 1: seconds -= 1
    else: seconds = 60

    time.sleep(t_dil)

import time
import math
from time import strftime, sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import qwiic_joystick

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

# Intialize buttons 
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Initialize Joystick
js = qwiic_joystick.QwiicJoystick()

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
font_r = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
isHomeScreen = True
r = 50

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    title = "Einstein's Clock"
    draw.text(((width-font.getsize(title)[0])/2, top+30), title, font=font, fill="#FFFFFF")
    disp.image(image, rotation)
    time.sleep(2)
    
    while isHomeScreen:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        
        # Display speed
        title = "Select speed"
        draw.text(((width-font.getsize(title)[0])/2, top+30), title, font=font, fill="#FFFFFF")
        text = str(r) + "%"
        draw.text(((width-font_r.getsize(text)[0])/2, bottom-60), text, font=font_r, fill="#888888")
        disp.image(image, rotation)
        
        if buttonB.value and not buttonA.value:  # just button A pressed
            time.sleep(0.2)
            print("Increase Speed")
            if r < 99: r+= 1
        if buttonA.value and not buttonB.value:  # just button B pressed
            time.sleep(0.2)
            print("Decrease Speed")
            if r > 1: r-=1
        if js.connected:
            r = round(js.vertical*98/1023) + 1
        
            if not js.button:
                time.sleep(0.2)
                isHomeScreen = False
                seconds = 60
        
        if not buttonA.value and not buttonB.value:  # Both pressed
            time.sleep(0.2)
            print("Start Game")
            isHomeScreen = False
            seconds = 60
    
    while seconds >= 0 and not isHomeScreen:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Calculate time dilation
        c = 300000 #Speed of light
        v = (r/100)*c #Traveler speed
        t_dil = 1 / math.sqrt((1-v**2/c**2)) #Time dilation
        
        # Display countdown
        y_label = top + (height - font.getsize(str(seconds))[1]) / 2 + 35
        x_label = 0 + (width - font.getsize(str(seconds))[0]) / 2
        draw.text((x_label,y_label), str(seconds), font=font, fill="#FFFFFF")
        
        tick = "."
        
        if seconds > 0:
            x_bar = 10
            y_bar = -10
            for i in range(seconds):
                if i > 19: break
                x_bar += font.getsize(tick)[0]
                draw.text((x_bar, y_bar), tick, font = font, fill = "#00FFFF")
       
        if seconds > 20:  
            x_bar = 10
            y_bar += font.getsize(tick)[1]
            for i in range(seconds - 20):
                if i > 19: break
                x_bar += font.getsize(tick)[0]
                draw.text((x_bar, y_bar), tick, font = font, fill = "#00FFFF")
                
        if seconds > 40:  
            x_bar = 10 
            y_bar += font.getsize(tick)[1]
            for i in range(seconds - 40):
                if i > 19: break
                x_bar += font.getsize(tick)[0]
                draw.text((x_bar, y_bar), tick, font = font, fill = "#00FFFF")
        
        # Display image.
        disp.image(image, rotation)
        
        #Counter
        if seconds >= 1: seconds -= 1
        else: isHomeScreen = True
        
        if not buttonA.value or not buttonB.value:
            isHomeScreen = True
        
        time.sleep(t_dil)

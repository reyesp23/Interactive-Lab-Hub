# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex5_binary_counter.py
#
# This example counts up from 0 to 1023 and displays the number in binary on the 
# LED Stick.
# --------------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# 
# This python library supports the SpakrFun Electronics qwiic sensor/
# board ecosystem on a Raspberry Pi (and compatible) board computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun by buying a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 5

from __future__ import print_function
import qwiic_led_stick
import time
import sys

def binary_LED_display(LED_stick, LED_length):
    # Create color arrays because we want to turn on whole string of LEDs at one time
    red_list = [0] * LED_length
    green_list = [0] * LED_length
    blue_list = [0] * LED_length
    
    # This for loop will repeat for each pixel of the LED Stick
    for i in range(0, 5):
        red_list[i] = 255
    LED_stick.set_all_LED_unique_color(red_list, green_list, blue_list, LED_length)
    time.sleep(0.1)

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 5")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")
    
    # Reset the state of LEDs
    my_stick.LED_off()

    while True:
        # This loop counts from 0 to 1023 and displays the binary over the 
        # serial port and the LED stick
     
        binary_LED_display(my_stick, 10)
            
    
if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 5")
        sys.exit(0)
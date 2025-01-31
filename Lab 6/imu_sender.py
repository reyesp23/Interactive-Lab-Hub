import time
import board
import busio
import adafruit_mpu6050
import paho.mqtt.client as mqtt
import uuid
import qwiic_led_stick

i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
my_stick = qwiic_led_stick.QwiicLEDStick()
if my_stick.begin() == False: print("\nThe Qwiic LED Stick isn't connected to the sytsem.")
my_stick.set_all_LED_brightness(10)

topic = 'IDD/imuTest'

def on_connect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    val = msg.payload.decode('UTF-8')
    rounded = round(float(val) * 1/2)
    display(rounded)
    # Turn on all the LEDs to white
    #my_stick.set_all_LED_brightness(10)

def display(value):
    # Create color arrays because we want to turn on whole string of LEDs at one time
    LED_length = 10
    red_list = [0] * LED_length
    green_list = [0] * LED_length
    blue_list = [0] * LED_length
    
    # This for loop will repeat for each pixel of the LED Stick
    for i in range(0, value):
        red_list[i] = 255
    my_stick.set_all_LED_unique_color(red_list, green_list, blue_list, LED_length)
 

# setup mqtt client
client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.connect('farlab.infosci.cornell.edu', port=8883)

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

while True:
    client.loop()
    val = mpu.acceleration
    client.publish(topic, abs(val[0]))
    time.sleep(0.25)
 

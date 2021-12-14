import time
from adafruit_servokit import ServoKit
import paho.mqtt.client as mqtt
import uuid
import text_draw 

text_draw.display_product_information('Shirt:Locked', "$2")
kit = ServoKit(channels=16)
servo = kit.servo[2]
servo.set_pulse_width_range(500, 2500)
topic = 'IDD/clotheslock/toggle/123'


def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	#Subscribe to the device topic


def on_message(cleint, userdata, msg):
	print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")

    # Set angle and update status on screen
	if msg.payload.decode('UTF-8') == '0': 
		servo.angle = 45
		text_draw.display_product_information('Shirt:Unlocked', "$2")
	else:
		text_draw.display_product_information('Shirt:Locked', "$2")
		servo.angle = 7
		

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')


client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)
client.loop_forever()

import time
import board
import busio
import adafruit_mpu6050
import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/imuTest'

i2c = busio.I2C(board.SCL, board.SDA)

mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    val = mpu.acceleration[0]
    print(val)
    client.publish(topic, val)
    time.sleep(0.25)

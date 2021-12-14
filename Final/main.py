from fastapi import FastAPI
import paho.mqtt.client as mqtt
import uuid

app = FastAPI()

@app.get("/")
async def helloWorld():
    return "hello world"

@app.get("/toggle/{deviceID}/{lockunlock}")
async def pushToggle(deviceID: str, lockunlock: str):
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')

    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)


    unlock_base = "IDD/clotheslock/toggle/"
    client.publish(f"{unlock_base}{deviceID}", lockunlock)
    return f"unlocked {deviceID}"

@app.get("/getProductInfo/{deviceID}")
async def getProductInfo(deviceID: str):
    return {"price": 10.99, "sale": None, "name": "Christmas Sock",  "store": {"storeInfo": "placeholder"}, "imageURL": "something"}

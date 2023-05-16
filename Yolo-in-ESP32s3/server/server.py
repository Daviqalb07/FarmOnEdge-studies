import paho.mqtt.client as mqtt 
from time import sleep
from config import *


client = mqtt.Client("Temperature_Inside")
client.connect(BROKER_IP, BROKER_PORT)

i=1
while True:
    data = f"i = {i}"
    client.publish("teste", data.encode('utf-8'))
    print("Just published " + data)
    i+=1
    sleep(1)
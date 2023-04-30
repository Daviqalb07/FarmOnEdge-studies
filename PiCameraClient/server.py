import os
import paho.mqtt.client as mqtt
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'images'

def main():
    client = mqtt.Client('server')
    client.connect(BROKER_IP, BROKER_PORT)
    
    client.on_message = on_message
    client.subscribe(IMAGES_TOPIC)

    client.loop_forever()

def on_message(client, userdata, message):
    image_bytes = message.payload
    image = Image.open(BytesIO(image_bytes))
    image.show()

main()
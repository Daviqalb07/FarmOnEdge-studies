import os
import paho.mqtt.client as mqtt
import datetime
from pymongo import MongoClient
from gridfs import GridFS
from io import BytesIO
from base64 import b64decode
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'images'

db = None

def main():
    global db
    
    client = start_client()

    client.on_message = on_message
    client.subscribe(IMAGES_TOPIC)

    db = mongo_conn()

    client.loop_forever()


def start_client() -> mqtt.Client:
    client = mqtt.Client()
    client.connect(BROKER_IP, BROKER_PORT)
    return client


def on_message(client, userdata, message):
    image_data = b64decode(message.payload)
    image_name = str(datetime.datetime.now())

    upload_image(image_data, image_name)


def mongo_conn():
    try:
        conn = MongoClient(host='127.0.0.1', port=27017)
        print("MongoDB connected", conn)
        return conn['images']
    
    except Exception as error:
        print(f"[ERROR] {error}")


def upload_image(image_data:bytes, filename:str):
    global db
    fs = GridFS(db)
    fs.put(image_data, filename=filename)


main()
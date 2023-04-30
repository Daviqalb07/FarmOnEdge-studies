import os
import paho.mqtt.client as mqtt
from io import BytesIO
from picamera import PiCamera
from time import sleep
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'images'

CAMERA_RESOLUTION = (1080, 720)
CAPTURE_PERIOD = 10 # in seconds

def start_camera(resolution: tuple, exposure_mode:str='auto') -> PiCamera:
    camera = PiCamera()
    camera.resolution = resolution
    camera.exposure_mode = exposure_mode
    return camera

def close_camera(camera: PiCamera):
    camera.close()

def capture(camera: PiCamera, image_stream: BytesIO, format='jpeg'):
    camera.capture(image_stream, format= format)

def read_image(image_stream: BytesIO) -> bytes:
    image_stream.seek(0)
    return image_stream.read()

def main():
    client = mqtt.Client('raspberrypi')
    client.connect(BROKER_IP, BROKER_PORT)

    camera = start_camera(CAMERA_RESOLUTION, exposure_mode='off')
    

    while True:
        try:
            image_stream = BytesIO()
            
            capture(camera, image_stream)
            
            image = read_image(image_stream)
            image_stream.close()
            client.publish(IMAGES_TOPIC, image)

            sleep(CAPTURE_PERIOD)
        except:
            close_camera(camera)
            break

        finally:
            image_stream.close()

main()
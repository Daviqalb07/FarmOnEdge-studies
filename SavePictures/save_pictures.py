import os
from datetime import datetime
from picamera import PiCamera
from time import sleep

CAMERA_RESOLUTION = (1280, 720)
CAPTURE_FORMAT = 'jpeg'
CAPTURE_PERIOD = 10

def main():
    camera = PiCamera(resolution=CAMERA_RESOLUTION)

    while True:
        save_dir = get_save_dir()        
        timestamp = datetime.now()
        filename = f'{ save_dir }/{ timestamp.strftime("%d-%m-%Y@%H_%M_%S") }.jpeg'

        try:
            camera.capture(filename, format=CAPTURE_FORMAT)
        except Exception as e:
            print(f'[ERROR] {e}')

        sleep(CAPTURE_PERIOD)


def get_save_dir():
    if os.path.exists('./usb/images'):
            save_dir = './usb/images'
    else:
        save_dir = './images'
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
    
    return save_dir


if __name__=="__main__":
    main()
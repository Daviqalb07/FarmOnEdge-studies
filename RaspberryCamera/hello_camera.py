import os
from picamera import PiCamera

path = './images'
if not os.path.exists(path):
	os.mkdir(path)

with PiCamera() as camera:
	camera.capture(f'{path}/hello.png')


import socket
from time import sleep
from picamera import PiCamera

SERVER_IP = '192.168.0.3'
SERVER_PORT = 8080
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

TIME_RECORDING = 120

client_socket = socket.socket()
client_socket.connect(SERVER_ADDRESS)
connection = client_socket.makefile('wb')

print('Connected to server!')

try:
    with PiCamera() as camera:
        camera.resolution = (1080, 720)
        camera.framerate = 30

        sleep(2)

        camera.start_recording(connection, format='h264')
        camera.wait_recording(TIME_RECORDING)
        camera.stop_recording()
finally:
    connection.close()
    client_socket.close()

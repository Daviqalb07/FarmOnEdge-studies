import socket
import subprocess

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8080
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

server_socket = socket.socket()
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(0)

connection = server_socket.accept()[0].makefile('rb')
try:
    cmd_line = ['vlc', '--demux', 'h264', '-']
    player = subprocess.Popen(cmd_line, stdin=subprocess.PIPE)

    while True:
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.terminate()

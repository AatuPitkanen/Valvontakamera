import socket
import subprocess
import os

# Start a socket listening for connections 
server_socket = socket.socket()
server_socket.bind((socket.gethostname(), 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    cmdline = ['C:/Users/Aatu/Documents/VLC/vlc.exe', '--demux', 'h264', '-'] #uses vlc for the video stream
    #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()    

import socket
import time
import picamera

client_socket = socket.socket()
client_socket.connect(('Ade', 8000))

connection = client_socket.makefile('wb')
try:
   with picamera.PiCamera() as camera:
        camera.resolution = (1024, 687)
        camera.framerate = 24
        
        camera.start_preview()
        time.sleep(2)

        camera.start_recording(connection, format='h264')
        camera.wait_recording(180) #test version streams for 3 minutes
        camera.stop_recording()

finally:
    connection.close()
    client_socket.close()

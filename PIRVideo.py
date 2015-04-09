import time
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)

with picamera.PiCamera() as camera:
  GPIO.wait_for_edge(4, GPIO.FALLING)
  print "Nauhoitus alkoi"
  camera.start_recording('/home/pi/Desktop/Foo.h264')
  camera.wait_recording(30)  
  camera.stop_recording()
  print "Nauhoitus paattyi"
  

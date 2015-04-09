import time
import picamera
import RPi.GPIO as GPIO

PIR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
def MOTION(PIR_PIN):
         print "Motion detected!"
print "PIR MODULE TEST"
time.sleep(1)
print "Readyyy"
try:
         GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
         while 1: 
                      time.sleep(1)
except Keyboardinterrupt:
            print "quit"
            GPIO.cleanup()

import time
import picamera
import RPi.GPIO as GPIO

import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.application import MIMEApplication

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN, GPIO.PUD_UP) #when infrared sensor detects movement start recording

with picamera.PiCamera() as camera:
   camera.resolution = (640, 480)
   GPIO.wait_for_edge(4,GPIO.FALLING)
   print "Nauhoitus alkoi"
   camera.start_recording('/home/pi/Desktop/Foo.h264')
   camera.wait_recording(30)
   camera.stop_recording()
   print "Nauhoitus paattyi"
   state = "Valmis"

if state == "Valmis":
   sender = 'embeddedkamera@gmail.com'
   receivers = ['myemail@gmail.com']

   message = MIMEMultipart()
   message['Subject'] = 'Valvontakamera'
   message['From'] = 'Raspi'
   message['To'] = 'Aatu'
   message.attach(MIMEApplication(open("/home/pi/Desktop/Foo.h264", "rb").read()))
   message.add_header('Content-Disposition', 'attachment', filename='Video.h264')

   username = 'embeddedKamera@gmail.com'
   password = 'password'

   Server = smtplib.SMTP('smtp.gmail.com:587')
   Server.starttls()
   Server.login(username,password)
   Server.sendmail(sender, receivers, message.as_string())
   print "Sahkoposti lahetetty!"
   Server.quit()


from Tkinter import *
import time
import picamera
import RPi.GPIO as GPIO
import socket
import RPi.GPIO as GPIO
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.application import MIMEApplication
d = time.strftime('%Y%m%d-%H%M%S')

class Application(Frame):
   
   def __init__(self, master):
       Frame.__init__(self,master)
       self.grid()
       self.create_widgets()

   def create_widgets(self):
       self.button1 = Button(self, text = "Start Email")
       self.button1["command"] = self.email
       self.button1.grid()

       self.button2 = Button(self, text = "Start Stream")
       self.button2["command"] = self.stream
       self.button2.grid()
      
       self.button3 = Button(self, text = "Take pictures")
       self.button3["command"] = self.picture
       self.button3.grid()
    
   def email(self):
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(4,GPIO.IN, GPIO.PUD_UP)

       with picamera.PiCamera() as camera:
           camera.resolution = (640, 480)
           GPIO.wait_for_edge(4,GPIO.FALLING)
           print "Nauhoitus alkoi"
           camera.start_recording('/home/pi/Desktop/Video.h264')
           camera.wait_recording(30)
           camera.stop_recording()
           print "Nauhoitus paattyi"
           state = "Valmis"

       if state == "Valmis":
            sender = 'embeddedkamera@gmail.com'
            receivers = ['aatu.pitkanen@hotmail.com']

            message = MIMEMultipart()
            message['Subject'] = 'Valvontakamera'
            message['From'] = 'Raspi'
            message['To'] = 'Aatu'
            message.attach(MIMEApplication(open("/home/pi/Desktop/Video.h264", "rb").read()))
            message.add_header('Content-Disposition', 'attachment', filename='Video.h264')

            username = 'username@gmail.com'
            password = 'password'
            Server = smtplib.SMTP('smtp.gmail.com:587') #Googles smtp server
            Server.starttls()
            Server.login(username,password)
            Server.sendmail(sender, receivers, message.as_string())
            print "Sahkoposti lahetetty!"
            Server.quit()
      
   def stream(self):
       client_socket = socket.socket()
       client_socket.connect(('Ade', 8000))

       connection = client_socket.makefile('wb')
       try:
          with picamera.PiCamera() as camera:
               camera.resolution = (1024, 687)
               camera.framerate = 24

               time.sleep(2)

               camera.start_recording(connection, format='h264')
               camera.wait_recording(180)
               camera.stop_recording()

       finally:
              connection.close()
              client_socket.close()
  
   def picture(self):
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)

       with picamera.PiCamera() as camera:
          time.sleep(2)
          GPIO.wait_for_edge(4, GPIO.FALLING) # wait until PIR-sensor in IO-pin 4 detects movement 
          print "Kuva otettu"
          camera.capture('/home/pi/Desktop/'+ d +'.jpg')

root = Tk()
root.title("Valvontakamera/Riistakamera")
root.geometry("300x100")
app = Application(root)
root.mainloop()


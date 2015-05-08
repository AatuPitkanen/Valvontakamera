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

       self.instuction = Label(self, text = "Enter sender email")
       self.instuction.grid(row = 0, column =0, columnspan = 2, sticky = W)

       self.instuction2 = Label(self, text = "Enter receiver email")
       self.instuction2.grid(row = 0, column =1, columnspan = 2, sticky = W)

       self.email = Entry(self)
       self.email.grid(row = 1, column = 0, sticky = W)

       self.receiver = Entry(self)
       self.receiver.grid(row = 1, column = 1, sticky = W)

       self.instruction2 = Label(self, text = "Enter sender password")
       self.instruction2.grid(row = 2, column = 0, sticky = W)

       self.password = Entry(self,show="*")
       self.password.grid(row = 3, column = 0, sticky = W)

       self.submit_button = Button(self, text = "Show Un/pw in console", command = self.add_email)
       self.submit_button.grid(row = 4, column = 0, sticky = W)
 
       self.label = Label(self, text = "Choose action")
       self.label.grid(row = 5, column = 0, sticky = W)

       self.button1 = Button(self, text = "Start Stream")
       self.button1["command"] = self.stream
       self.button1.grid()

       self.button2 = Button(self, text = "Take Videos")
       self.button2["command"] = self.video
       self.button2.grid()
      
       self.button3 = Button(self, text = "Take pictures")
       self.button3["command"] = self.picture
       self.button3.grid()
       
       self.button4 = Button(self, text = "Email picture")
       self.button4["command"] = self.email_picture
       self.button4.grid()
       
       self.button5 = Button(self, text = "Email video")
       self.button5["command"] = self.email
       self.button5.grid()       

   def add_email(self):
       username = self.email.get()
       password = self.password.get()
       receivers =  self.receiver.get()
       print "Username: "+username+"|"+"Password: " + password + "|"+"Receiver: "+ receivers


   def video(self):
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(4,GPIO.IN, GPIO.PUD_UP)
       with picamera.PiCamera() as camera:
	 video = 1
	 while video == 1:
	   camera.resolution = (640, 480)
           GPIO.wait_for_edge(4,GPIO.FALLING)
	   print "Nauhoitus alkoi"
	   camera.start_recording('/home/pi/Desktop/'+d+'.h264')
	   camera.wait_recording(60)
	   camera.stop_recording()
	   print "Video valmis"
    
   def email(self):
       username = self.email.get()
       password = self.password.get()
       receivers =  self.receiver.get()

       GPIO.setmode(GPIO.BCM)
       GPIO.setup(4,GPIO.IN, GPIO.PUD_UP)

       with picamera.PiCamera() as camera:
          loop = 1
          while loop == 1:
	           camera.resolution = (640, 480)
	           GPIO.wait_for_edge(4,GPIO.FALLING)
	           print "Nauhoitus alkoi"
	           camera.start_recording('/home/pi/Desktop/Foo.h264')
        	   camera.wait_recording(30)
          	   camera.stop_recording()
	           print "Nauhoitus paattyi"
	           state = "Valmis"

	           if state == "Valmis":
	           
	           
	            message = MIMEMultipart()
       		    message['Subject'] = 'Valvontakamera Video'
	            message['From'] = 'Raspi'
	            message['To'] = email
	            message.attach(MIMEApplication(open("/home/pi/Desktop/Foo.h264", "rb").read()))
	            message.add_header('Content-Disposition', 'attachment', filename="Video.h264")
	
	            Server = smtplib.SMTP('smtp.gmail.com:587')
	            Server.starttls()
	            Server.login(username,password)
	            Server.sendmail(email, receivers, message.as_string())
	            print "Sahkoposti lahetetty!"
	            Server.quit()
      
   def stream(self):
       client_socket = socket.socket()
       client_socket.connect((socket.gethostname(), 8000))

       connection = client_socket.makefile('wb')
       try:
          with picamera.PiCamera() as camera:
               camera.resolution = (640, 480)
               camera.framerate = 24

               time.sleep(2)

               camera.start_recording(connection, format='h264')
               camera.wait_recording(180)
               camera.stop_recording()

       finally:
              connection.close()
              client_socket.close()

   def email_picture(self):
     username = self.email.get()
     password = self.password.get()
     receivers =  self.receiver.get()

     GPIO.setmode(GPIO.BCM)
     GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)
     with picamera.PiCamera() as camera:
      time.sleep(1)
      kuva = 1
      while kuva == 1:
        GPIO.wait_for_edge(4, GPIO.FALLING)
        print "Kuva otettu"
        camera.capture("/home/pi/Desktop/Testi.jpg")
        state = "valmis"

        if state == "valmis":
          
           message = MIMEMultipart()
           message['Subject'] = 'Valvontakamera Valokuva'
           message['From'] = 'Raspi'
           message['To'] = email
           message.preamble = "Photo @ "
           fp = open("/home/pi/Desktop/Testi.jpg", "rb")
           img = MIMEImage(fp.read())
           fp.close()
           img.add_header('Content-Disposition', 'attachment', filename=d + ".jpg")
           message.attach(img)

           Server = smtplib.SMTP('smtp.gmail.com:587')
           Server.starttls()
           Server.login(username,password)
           Server.sendmail(email, receivers, message.as_string())

           Server.quit()

   def picture(self):
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)

       with picamera.PiCamera() as camera:
	kuva = 1
	while kuva == 1:
          time.sleep(1)
          GPIO.wait_for_edge(4, GPIO.FALLING)
          print "Kuva otettu"
          camera.capture('/home/pi/Desktop/'+ d +'.jpg')

root = Tk()
root.title("Valvontakamera/Riistakamera")
root.geometry("350x300")
app = Application(root)
root.mainloop()


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

class Application(Frame):
   
   def __init__(self, master):
       Frame.__init__(self,master)
       self.grid()
       self.create_widgets()

   def create_widgets(self):

       self.instuction = Label(self, text = "Enter sender email")
       self.instuction.grid(row = 0, column =0, columnspan = 2, sticky = W)
       self.instuction6 = Label(self, text = "Enter receiver email")
       self.instuction6.grid(row = 0, column =2, columnspan = 2, sticky = W)  
       self.instruction2 = Label(self, text = "Enter sender password")
       self.instruction2.grid(row = 0, column = 1, sticky = W)
  
       self.email = Entry(self)
       self.email.grid(row = 1, column = 0, sticky = W)
       self.password = Entry(self,show="*")
       self.password.grid(row = 1, column = 1, sticky = W)
       self.receiver = Entry(self)
       self.receiver.grid(row = 1, column = 2, sticky = W)

       self.submit_button = Button(self, text = "Show Un/pw in console", command = self.add_email)
       self.submit_button.grid(row = 4, column = 0, sticky = W)
       self.label = Label(self, text = "Choose action")
       self.label.grid(row = 5, column = 0, sticky = W)

       self.button1 = Button(self, text = "Start Stream")
       self.button1["command"] = self.stream
       self.button1.grid(row = 6, column = 0, sticky = W)
       
       self.instruction3 = Label(self, text = "Stream host address")
       self.instruction3.grid(row = 2, column = 0, sticky = W)
       self.instruction4 = Label(self, text = "Stream host port")
       self.instruction4.grid(row = 2, column = 1, sticky = W)

       self.addr = Entry(self)
       self.addr.grid(row = 3, column = 0, sticky = W)
       self.port = Entry(self)
       self.port.grid(row = 3, column = 1, sticky = W)

       self.button2 = Button(self, text = "Take Videos")
       self.button2["command"] = self.video
       self.button2.grid(row = 7, column = 0, sticky = W)
      
       self.button3 = Button(self, text = "Take pictures")
       self.button3["command"] = self.picture
       self.button3.grid(row = 8, column = 0, sticky = W)
       
       self.button4 = Button(self, text = "Email pictures")
       self.button4["command"] = self.email_picture
       self.button4.grid(row = 9, column = 0, sticky = W)
       
       self.button5 = Button(self, text = "Email videos")
       self.button5["command"] = self.email_video
       self.button5.grid(row = 10 , column = 0, sticky = W)       

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
           d = time.strftime('%a, %d %b %Y %H:%M:%S')
	   camera.resolution = (640, 480)
           GPIO.wait_for_edge(4,GPIO.FALLING)
	   print "Nauhoitus alkoi"
	   camera.start_recording('/home/pi/Desktop/camera/'+d+'.h264')
	   camera.wait_recording(60)
	   camera.stop_recording()
	   print "Video valmis"
	   time.sleep(3)
    
   def email_video(self):
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
	           camera.start_recording('/home/pi/Desktop/camera/Foo.h264')
        	   camera.wait_recording(30)
          	   camera.stop_recording()
	           print "Nauhoitus paattyi"
	           state = "Valmis"
	           if state == "Valmis":
	     
	            message = MIMEMultipart()
       		    message['Subject'] = 'Valvontakamera Video'
	            message['From'] = 'Raspi'
	            message['To'] = receivers
	            message.attach(MIMEApplication(open("/home/pi/Desktop/camera/Foo.h264", "rb").read()))
	            message.add_header('Content-Disposition', 'attachment', filename="Video.h264")
	            Server = smtplib.SMTP('smtp.gmail.com:587')
	            Server.starttls()
	            Server.login(username,password)
	            Server.sendmail(username, receivers, message.as_string())
	            print "Sahkoposti lahetetty!"
	            Server.quit()
      
   def stream(self):
       hostname = str(self.addr.get())
       port = int(self.port.get())
       client_socket = socket.socket()
       client_socket.connect((hostname, port))
       connection = client_socket.makefile('wb')
       try:
          with picamera.PiCamera() as camera:
               camera.resolution = (640, 480)
               camera.framerate = 24

               time.sleep(2)

               camera.start_recording(connection, format='h264')
               camera.wait_recording(604800)
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
	d = time.strftime('%a, %d %b %Y %H:%M:%S')
	GPIO.wait_for_edge(4, GPIO.FALLING)
        for x in xrange(0,4):
		 x = x + 1
       		 camera.capture("/home/pi/Desktop/camera/"+str(x)+".jpg")
        message = MIMEMultipart()
        message['Subject'] = 'Valvontakamera Valokuva'
        message['From'] = 'Raspi'
        message['To'] = str(receivers)
        message.preamble = "Photo @ "
        fp = open("/home/pi/Desktop/camera/1.jpg", "rb")
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-Disposition', 'attachment', filename=d +"-"+str(1)+ ".jpg")
        message.attach(img)
        
        fp = open("/home/pi/Desktop/camera/2.jpg", "rb")
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-Disposition', 'attachment', filename=d +"-"+str(2)+ ".jpg")
        message.attach(img)
        fp = open("/home/pi/Desktop/camera/3.jpg", "rb")
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-Disposition', 'attachment', filename=d +"-"+str(3)+ ".jpg")
        message.attach(img)
        fp = open("/home/pi/Desktop/camera/4.jpg", "rb")
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-Disposition', 'attachment', filename=d +"-"+str(4)+ ".jpg")
        message.attach(img)

        Server = smtplib.SMTP('smtp.gmail.com:587')
        Server.starttls()
        Server.login(username,password)
        Server.sendmail(username, receivers, message.as_string())
	print "email sent!"
	Server.quit()

   def picture(self):
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(4, GPIO.IN, GPIO.PUD_UP)
       with picamera.PiCamera() as camera:
	kuva = 1
	while kuva == 1:
	  d = time.strftime('%a, %d %b %Y %H:%M:%S')
	  GPIO.wait_for_edge(4, GPIO.FALLING)
          print "Kuva otettu"
          camera.capture('/home/pi/Desktop/camera/'+d+'.jpg')

   def __del__(self,type, value, traceback):
	 print 'died'

root = Tk()
root.title("Valvontakamera/Riistakamera")
root.geometry("500x300")
app = Application(root)
root.mainloop()

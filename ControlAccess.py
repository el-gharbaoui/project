# coding:utf-8
#!/usr/bin/python
from requests import get
from threading import  Thread,RLock
from time import sleep
import time,sys,socket,requests
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
redPin=25
greenPin=24
bluePin=23

def turnOff(pin):
    #GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)
    #print("Led {} Eteint:".format(couleur))

def blink(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,0)
    #print("Led {} Allume:".format(couleur))
def whiteOn():
	turnOff(redPin)
	turnOff(greenPin)
	turnOff(bluePin)
	
def redOn():
	blink(redPin)
	
def greenOn():
	blink(greenPin)

def blueOn():
	blink(bluePin)
	
def yellowOn():
	blink(redPin)
	blink(greenPin)
def whiteOff():
	blink(redPin)
	blink(greenPin)
	blink(bluePin)
def redOff():
	turnOff(redPin)

def greenOff():
	turnOff(greenPin)

def blueOff():
	turnOff(bluePin)

def yellowOff():
	turnOff(redPin)
	turnOff(greenPin)
    
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)    

rbnom=str(socket.gethostname())

modedebug=True

def declancherrelay(port):
            if modedebug==True:
                print("Roulet Allume")
                GPIO.output(port, True)
                GPIO.output(greenPin,0)
                time.sleep(2) # On attend le temps defini
                print("Roulet Eteint")
                GPIO.output(port, False)
                GPIO.output(greenPin,1)
                time.sleep(1)
                
               
                
                
def declancheled(port,couleur):
        if modedebug==True:
                print("Led {} Allume:".format(couleur))
                GPIO.output(port,0)
                time.sleep(2) # On attend le temps defini
                GPIO.output(port, 1)
                time.sleep(2) 
##              print("Led {} Eteint:".format(couleur))
            
            
class MonThread (Thread):
    def __init__(self,Codebarre):
        Thread.__init__(self)
        self.Codebarre=Codebarre
        
     
  #sudo python /home/pi/ControlAccess.py &
        
    def run(self):
                url="http://aex.e-maroc.info/CHECK/"+rbnom+":"+self.Codebarre
                content=requests.get(url)
                 #Allumer led Vert(eclanche roulet)  
                if (content.text.find('OK')!=(-1)):#acces accepté
                    roulet=21
                    declancherrelay(roulet)
                    print(content.text+" Access granted :")
                 #Allumer led Orange  
                elif (content.text.find('SOON')!=(-1)):#acces sera réglé
                        declancheled(bluePin,"Orange")
                        print(content.text+" Access Soon:")
                        
                 #Allumer led Rouge  
                else:#//Refuse d'acces
                        declancheled(redPin,"Rouge")
                        print(content.text+" Access denied:")
                        
                time.sleep(2)
                whiteOn()       
                
                   
###Allumer led rouge     


#declencher roulet
roulet=21
declancherrelay(roulet)

# time to sleep between operations in the main loop

SleepTimeL = 2

try:
    while 1:
            
        Codebarre = sys.stdin.readline()
        #Codebarre =sys.stdout.flush()
        Codebarre = Codebarre.replace('\n','')
    # Création de thread
        m = MonThread(Codebarre)
    # Lancement des threads
        m.start()
    
except KeyboardInterrupt:
    print ("\nExit")
     # Reset GPIO settings  
    GPIO.cleanup()
   
     
      
   
  
# coding:utf-8
#!/usr/bin/python
# System modules
from requests import get
from queue import Queue
from threading import  Thread
import time,sys,socket,requests
import RPi.GPIO as GPIO
import threading
import queue

rbnom=str(socket.gethostname())
q = queue.Queue()

# Set up some global variables
encore = True
time_sleep_led=5
time_sleep_relay=1
redPin=25
greenPin=24
bluePin=23

def turnOff(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)
    
def blink(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,0)
     
def redOn():
	blink(redPin)
	
def greenOn():
	blink(greenPin)   

def blueOn():
	blink(bluePin)
	
def redOff():
	turnOff(redPin)
	
def greenOff():
	turnOff(greenPin)
	
def blueOff():
	turnOff(bluePin)
	
def declencherelay():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, True)
    time.sleep(time_sleep_relay)#attend 1 secondes sans rien faire
    GPIO.output(21, False)
#oldcb="MRR07M0346"
def worker():
    oldcb =""
    while 1:
       
        #Lecteur code barre python
        codebarre=sys.stdin.readline().rstrip('\n')
        #print(codebarre)
        if(codebarre != oldcb):
            oldcb=codebarre
            #Put codebarre into the queue
            q.put(codebarre)
        else:
            print("exist deja")
                
#queues = []
            

# crée le thread  
w = threading.Thread(name='worker', target=worker)
# démarre le thread 
w.start()
    
print('debut')


while encore:
    # print('.')
    if not q.empty():
        cb=q.get()
        url="http://aex.e-maroc.info/CHECK/"+rbnom+":"+cb
        content=requests.get(url)
        
        # OK ALLUMER LED VERT 
        if(content.text.find('OK')!=(-1)):
            greenOn()
            #DECLENCHER RELEY
            t = threading.Thread(name='declencherelay', target=declencherelay).start()
            time.sleep(time_sleep_led)
            greenOff()
            #NEAR ALLUMER LED bleu
        elif (content.text.find('SOON')!=(-1)):
            blueOn()
            time.sleep(time_sleep_led)
            blueOff()
            #BAD ALLUMER LED ROUGE
        elif (content.text.find('ALREADY')!=(-1)):
             redOn()
             time.sleep(time_sleep_led)
             redOff()            
        else:
            print('une erreur est survenue')
            
        print(time.asctime(time.localtime(time.time())), ' > CB:', cb, ' Queued remains : ' , q.qsize())
    else:
        print(time.asctime(time.localtime(time.time())), ' > None')
    time.sleep(time_sleep_led)
  

        

   

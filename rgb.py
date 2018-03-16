import RPi.GPIO as GPIO                                               # Importation des librairies qui gerent les ports
import time

GPIO.setmode(GPIO.BCM)

RED = 25
GREEN = 24
BLUE = 23

GPIO.setwarnings(False)
GPIO.setup(RED,GPIO.OUT)
GPIO.output(RED,0)
GPIO.setwarnings(False)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.output(GREEN,0)
GPIO.setwarnings(False)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.output(BLUE,0)

##RGB=[11,13,15]
##for pin in RGB:
##    GPIO.setup(pin, GPIO.OUT)
##    GPIO.output(pin,1)

try:
    while True:
        request =input("RGB-->")#101 ou 010 ou 011 ou 110 ou 111 ou 000
        if len(request) == 3:
            
             GPIO.output(RED,int(request[0]))#For red write 100 and after click enter
             GPIO.output(GREEN,int(request[1]))#For green write 010 and after click enter
             GPIO.output(BLUE,int(request[2]))#For blue write 001 and after click enter
             
except KeyboardInterrupt:
    GPIO.cleanup()
    print ("\nExit")


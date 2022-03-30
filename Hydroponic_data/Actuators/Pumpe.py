import RPi.GPIO as GPIO #importerer GPIO funktionalitet, gør vi fordi RPi kun har digital pins GPIO= General Purpose In Out 
import time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = 26
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on

while True:
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) #Tænd funktion 
    print("sætter til HIGH")
    time.sleep(2700) #Kører i 45 minutter
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) #Sluk funktion 
    print("sætter til LOW")
    time.sleep(1800) #"sover" i 30 minutter 
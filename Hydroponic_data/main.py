import time #importerer tidsbibliokteket fra RPi interne bibliotek
import sqlite3 #importerer sqlite, som er en database applikation
import Adafruit_DHT #importerer adafruit DHT bibliotek 
import Sensor_kode.Ultra as Ultra #eget selvskrevende - sensor bibliotek for den ultrasoniske sensor (vores afstandsmåler/vandstand)  
import Sensor_kode.Lys_main as Lys_main #eget selskrevet - sensor biblioteket til lyssensor(photoresistor) 
import RPi.GPIO as GPIO #importerer GPIO funktionalitet, gør vi fordi RPi kun har digital pins


#Database navn 
dbname='sensorsData.db' #navnet på databasen dbname = databasenavn. 
#Running interval
sampleFreq = 10 #Det interval main.py bliver afviklet i - generel sleep funktion. 
Lampe = Lys_main.KAmodRPiADCDAC().readMCP3021()

#RGB LYS
LED_ROED = 19 #Pinout til trafiklyset
LED_GUL = 13 #Pinout til trafiklyset
LED_GROEN = 5 #Pinout til trafiklyset

#HVID LED LYS
LED = 6 #Pinout til LED

#Set RGB LED pin som output
GPIO.setmode(GPIO.BCM) #BCM = board mode, RPi's pre-definition af pins. ********
GPIO.setup(LED_ROED, GPIO.OUT) #Sætter pin til output
GPIO.setup(LED_GUL, GPIO.OUT)
GPIO.setup(LED_GROEN, GPIO.OUT)

#Set LED pin som output
GPIO.setup(LED, GPIO.OUT) #Sætter pin til output



# get data from DHT sensor - trækker dataen ud
def getDHTdata(): #Vi laver funktionen getDHTdata 
	DHT11Sensor = Adafruit_DHT.DHT11 #Sætter sensor input fra Adafruit DHT biblioteket, og definerer at det er til DHT11 og ikke DHT22. 
	DHTpin = 16
	hum, temp = Adafruit_DHT.read_retry(DHT11Sensor, DHTpin) #hum, temp egne variabler - henter værdier fra DHT11sensor og fra DHTpin(16)
	if hum is not None and temp is not None: # hvis dine to værdier ikke er værdier gør følgende: 
		hum = round(hum) #Aflæser hum round = at der ikke kommer decimaler ******
		temp = round(temp, 1) #Aflæser temp round,1 = at der kommer hel tal ******
	return temp, hum #retuner værdier temp og hum, så vi kan kalde dem igen og få nye aflæsninger. De ryger tilbage i funktionen

temp, hum = getDHTdata() #for at funktionaliteten på log data, definer vi funktionen getDHTdata, som temp og hum. 

#Data log funktion for temperatur og fugtighed værdier
def logData_DHT (temp, hum): #opretter funktionen, som skal trække data fra getDHTdata 
	conn=sqlite3.connect(dbname) #sqlite3 funktionaliteten, hvor vi bruger connect som connecter til vores database 
	curs=conn.cursor() #Curs = hvordan den skal sætte ting ind i database, hvor det skal hen
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum)) #Sætter daten ind i de korrekte tabeller 
	conn.commit() #Nu er dataen placeret korrekt og der gemmes
	conn.close() #Afbryder forbindelsen til databasen
	return temp, hum

#Data log funktion for vand værdier
def logData_VAND():
	vand = Ultra.distance()
	vand = "{0:.2f}".format(vand) #formateringsstreng, hvor den cutter tallene ned, så der ikke er for mange decimaler 
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO vand_data values(datetime('now'), (?))", (vand,))
	conn.commit()
	conn.close()
	return vand

#Data log funktion for lys værdier
def logData_Lys ():
    Lampe = Lys_main.KAmodRPiADCDAC().readMCP3021() #Vi henviser til lys.main filen, kalder class(KAmodRPiADCDAC), inden i class kaldes funktionen readMCP
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO lys_data values(datetime('now'), (?))", (Lampe,))
	conn.commit()
	conn.close()
	return Lampe


while True: 
	#Data logging: lavet funktioner, alt hvad vi sender til databasen 
	logData_VAND() 
	logData_DHT(temp, hum)
	logData_Lys(Lampe)
	print(logData_Lys) 

	#RGB LED LYS: spand 12 cm. 
	if Ultra.distance() > 0 and Ultra.distance() < 3:
		GPIO.output(LED_ROED, False)
		GPIO.output(LED_GUL, False)
		GPIO.output(LED_GROEN, True)
	if Ultra.distance() > 3.1 and Ultra.distance() < 4:
		GPIO.output(LED_ROED, False)
		GPIO.output(LED_GUL, True)
		GPIO.output(LED_GROEN, False)
	if Ultra.distance() > 6:
		GPIO.output(LED_ROED, True)
		GPIO.output(LED_GUL, False)
		GPIO.output(LED_GROEN, False)

	#HVID LED LYS:
	if Lampe < 1650:
		GPIO.output(LED, True)
	if Lampe > 1650:
		GPIO.output(LED, False)
	#Tidsinterval for while True:
	time.sleep(sampleFreq) #Defineret i toppen 

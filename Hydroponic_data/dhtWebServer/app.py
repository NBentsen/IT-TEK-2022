from flask import Flask, render_template, request #Importere flask modulet og render_template som trækker vores index.html ind 
app = Flask(__name__) #definere vores app til at være flask 

import sqlite3 #defineret i main.py, en database motor/bibliotek 

# Retrieve data from database
def getDHTData():
	conn=sqlite3.connect('Hydroponic_data/sensorsData.db') #her connecter vi til de ønskede database rækker
	curs=conn.cursor() 

	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"): #Her vælger vi hvor alt vores data skal placeres i databasen i hvilken rækkefølge 
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	conn.close() #afbryder forbindelsen
	return time, temp, hum  #returnere værdierne 

def getULTRAData(): 
	conn=sqlite3.connect('Hydroponic_data/sensorsData.db')
	curs=conn.cursor()

	for row in curs.execute("SELECT * FROM vand_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		vand = row[1]
	conn.close()
	return time, vand

def getLYSData():
	conn=sqlite3.connect('Hydroponic_data/sensorsData.db')
	curs=conn.cursor()

	for row in curs.execute("SELECT * FROM lys_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		lys = row[1]
	conn.close()
	return time, lys

# main route 
@app.route("/") #app = flask 
def index(): #opretter funktion index 
	
	timedht, temp, hum = getDHTData() #tager alle variabler og definere til kaldefunktioner 
	timevand, vand = getULTRAData()
	timelys, lys = getLYSData()
	templateData = { #Variabler vi definerer 
	  'time'	: timedht,
      'temp'	: temp,
      'hum'		: hum,
	  'timevand': timevand,
      'vand'	: vand,
	  'timelys'	: timelys,
      'lys'		: lys
	}
	return render_template('index.html', **templateData) #returnere værdier 

if __name__ == '__main__': #hvis flask = main, så runner den vores app
    app.run(debug=False, port=8000, host='192.168.137.189') #Beder om at runne flask og vi har givet den nogle loaded værdier, vi har ændret portnummer til en ikke dedikeret port (8000) er en åben/fri port 
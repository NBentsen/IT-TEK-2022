from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

# Retrieve data from database
def getDHTData():
	conn=sqlite3.connect('Hydroponic_data/sensorsData.db')
	curs=conn.cursor()

	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
		hum = row[2]
	conn.close()
	return time, temp, hum

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
@app.route("/")
def index():
	
	timedht, temp, hum = getDHTData()
	timevand, vand = getULTRAData()
	timelys, lys = getLYSData()
	templateData = {
	  'time'	: timedht,
      'temp'	: temp,
      'hum'		: hum,
	  'timevand': timevand,
      'vand'	: vand,
	  'timelys'	: timelys,
      'lys'		: lys
	}
	return render_template('index.html', **templateData)

if __name__ == '__main__':
    app.run(debug=False, port=8000, host='192.168.137.189')
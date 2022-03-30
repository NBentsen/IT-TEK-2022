import sqlite3 as lite #Script til at lave database automatisk, intet er lavet i terminal 
import sys
con = lite.connect('sensorsData.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS DHT_data")
    cur.execute("CREATE TABLE DHT_data(timestamp DATETIME, temp NUMERIC, hum NUMERIC)") #NUMERIC = 
    cur.execute("DROP TABLE IF EXISTS vand_data")
    cur.execute("CREATE TABLE vand_data(timestamp DATETIME NUMERIC, Vand REAL)") #REAL = 
    cur.execute("DROP TABLE IF EXISTS lys_data")
    cur.execute("CREATE TABLE lys_data(timestamp DATETIME, LYSE TEXT)") #TEXT = at værdierne kommer i en string 
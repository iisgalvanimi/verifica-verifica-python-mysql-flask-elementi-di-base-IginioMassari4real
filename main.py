import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Animali")
mycursor.execute("USE Animali")
mycursor.execute("CREATE TABLE mammiferi (id INT AUTO_INCREMENT PRIMARY KEY, nome_comune VARCHAR(255), ordine VARCHAR(255), dimensioni VARCHAR(255), habitat VARCHAR(255), alimentazione VARCHAR(255))")
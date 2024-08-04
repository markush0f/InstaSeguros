import mysql.connector as connector

mydb = connector.connect(
    host="localhost",
    user="root",
    password="1234",
)

mycursor = mydb.cursor()

# mycursor.execute("DROP DATABASE IF EXISTS InstaSeguros")
mycursor.execute("CREATE DATABASE IF NOT EXISTS InstaSeguros")

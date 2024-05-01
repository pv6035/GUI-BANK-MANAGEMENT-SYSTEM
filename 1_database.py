import mysql.connector as sql
from mysql.connector import Error

conn = sql.connect(host="localhost", user="root", passwd="root@123")
mycursor = conn.cursor() #creating a cursor object of the name 'mycursor'.

SQL_cmd1 = "CREATE DATABASE the_royal_bank" #MySQL query to create database of the name 'the_royal_bank'.

try: #try block to run the code if it's right.
    mycursor.execute(SQL_cmd1) #Executing the MySQL query.
    print("Query OK, database, 'the_royal_bank' added.")
except sql.Error as err: #except block to show the error msg if the database already exist.
    print(err)

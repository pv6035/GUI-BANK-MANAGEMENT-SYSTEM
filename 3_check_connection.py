import mysql.connector as sql
from mysql.connector import Error

try:
     conn = sql.connect(host="localhost", user="root", passwd="root@123", database="the_royal_bank")
     if conn.is_connected(): #checks whether the connection to MySQL is available, returns True when the connection is available, False otherwise.
          print("Connection Successful.")
          db_Info = conn.get_server_info()
          print("Connected to MySQL Server version: ", db_Info) #prints the MySQL server version which you are running.
          mycursor = conn.cursor()
          mycursor.execute("select database();")
          record = mycursor.fetchone()
          print("You're connected to database: ", record) #prints the name of the database to which you are connected to.

except Error as err:
    print("Error while connecting to MySQL", err)
